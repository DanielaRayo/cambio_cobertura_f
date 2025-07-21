# coding: utf-8

# In[1]:


import geopandas as gpd      # Para manejar datos espaciales (shapefiles, geometría)
import pandas as pd          # Para manejar datos tabulares


# In[2]:
def definir_rutas():

    from pathlib import Path 
    """
    Define rutas absolutas a los archivos necesarios.
    Usa /notebooks/docs si existe, o usa el directorio actual si no.
    Valida existencia de archivos y muestra info útil.
    """
    
    root = Path("/notebooks/docs") if Path("/notebooks/docs").exists() else Path.cwd()

    print(f"📁 Carpeta raíz utilizada: {root.resolve()}")

    rutas = {
        "SHAPE_MUN": root / "municipios_colombia.shp",
        "EVA_CSV":   root / "Evaluaciones_Agropecuarias_Municipales_EVA.csv",
        "EST_CSV":   root / "Catalogo_Estaciones_IDEAM.csv",
        "RUNAP":     root / "runap.shp"
    }

    # Verifica que los archivos existen
    for nombre, ruta in rutas.items():
        if not ruta.exists():
            print(f"⚠️ Advertencia: el archivo {ruta.name} no se encuentra en {ruta.parent}")
        else:
            print(f"✅ {nombre} encontrado en {ruta}")

    return rutas


# In[3]:


def cargar_datos(rutas):
    print("🔄 Cargando datos...")

    # Usa las rutas pasadas en el diccionario
    gdf_mun = gpd.read_file(rutas["SHAPE_MUN"]).to_crs(epsg=9377)

    codigo_col = "Codigo_Mun" if "Codigo_Mun" in gdf_mun.columns else "MPIO_CCDGO"
    gdf_mun["MPIO_CCDGO"] = gdf_mun[codigo_col].astype(str).str.zfill(5)

    eva = pd.read_csv(rutas["EVA_CSV"])
    eva.rename(columns=lambda x: x.strip(), inplace=True)
    eva.rename(columns={"CÓD. MUN.": "cod_mun"}, inplace=True)
    eva["cod_mun"] = eva["cod_mun"].astype(str).str.zfill(5)

    df_est = pd.read_csv(rutas["EST_CSV"], sep=";", encoding="latin1")
    df_est = df_est[df_est["Estado"] == "Activa"].copy()
    coords = df_est["Ubicación"].str.strip("()").str.split(",", expand=True).astype(float)
    df_est["lat"], df_est["lon"] = coords[0], coords[1]

    gdf_est = gpd.GeoDataFrame(df_est,
        geometry=gpd.points_from_xy(df_est["lon"], df_est["lat"]),
        crs="EPSG:4326").to_crs(epsg=9377)

    gdf_runap = gpd.read_file(rutas["RUNAP"]).to_crs(epsg=9377)

    print(f"✅ Cargado: {len(gdf_mun):,} municipios • {len(gdf_est):,} estaciones • {len(eva):,} EVA • {len(gdf_runap):,} RUNAP")
    return gdf_mun, eva, gdf_est, gdf_runap


# In[4]:


def calcular_produccion_avocado(eva, anio=2018):
    print("📊 Procesando producción de aguacate...")

    # Filtramos cultivos relacionados con "AGUACATE" sin importar mayúsculas/minúsculas
    df = eva[eva["CULTIVO"].str.upper().str.contains("AGUACATE", na=False)].copy()

    # Si se especifica el año, filtramos solo ese año
    if anio:
        df = df[df["AÑO"] == anio]
        print(f"📆 Filtrando por año: {anio}")

    # Convertimos las columnas de área sembrada y producción a valores numéricos
    df["area_ha"] = pd.to_numeric(df["Área Sembrada\n(ha)"], errors="coerce")
    df["produccion_t"] = pd.to_numeric(df["Producción\n(t)"], errors="coerce")

    # Eliminamos filas con valores nulos
    df.dropna(subset=["area_ha", "produccion_t"], inplace=True)

    # Agrupamos por municipio y sumamos los valores
    resumen = df.groupby("cod_mun").agg(
        area_ha=("area_ha", "sum"),
        produccion_t=("produccion_t", "sum")
    ).reset_index()

    # Calculamos el rendimiento (producción / área)
    resumen["rendimiento_t_ha"] = resumen["produccion_t"] / resumen["area_ha"]

    # Normalizamos código de municipio
    resumen.rename(columns={"cod_mun": "MPIO_CCDGO"}, inplace=True)
    resumen["MPIO_CCDGO"] = resumen["MPIO_CCDGO"].astype(str).str.zfill(5)

    print(f"✅ {len(resumen)} municipios con producción registrada")
    return resumen


# In[5]:


def contar_estaciones_activas(gdf_est, gdf_mun):
    print("📡 Procesando estaciones IDEAM...")

    # Unimos estaciones con municipios para saber en qué municipio está cada estación
    join = gpd.sjoin(gdf_est, gdf_mun[["MPIO_CCDGO", "geometry"]], predicate="within", how="inner")

    # Contamos el número de estaciones por municipio
    conteo = join.groupby("MPIO_CCDGO").size().reset_index(name="num_estaciones")

    print(f"✅ {len(conteo)} municipios con estaciones IDEAM")
    return conteo


# In[6]:


def evaluar_superposicion_runap(gdf_runap, gdf_mun):
    print("🌱 Procesando áreas RUNAP...")

    # Intersecamos polígonos de RUNAP con municipios para ver qué tanto se superponen
    inter = gpd.overlay(
        gdf_runap,
        gdf_mun[["MPIO_CCDGO", "geometry"]],
        how="intersection",
        keep_geom_type=False  # Permitimos geometrías mixtas para no perder información
    )

    # Calculamos área protegida en m² por municipio
    inter["area_runap_m2"] = inter.area
    resumen = inter.groupby("MPIO_CCDGO")["area_runap_m2"].sum().reset_index()

    print(f"✅ {len(resumen)} municipios con presencia RUNAP")
    return resumen


# In[7]:


def calcular_score_final(gdf_mun, df_prod, df_est, df_runap):
    print("🧮 Calculando SCORE final...")

    # Partimos del listado de municipios únicos
    base = gdf_mun[["MPIO_CCDGO", "MPIO_CNMBR"]].drop_duplicates().copy()

    # Unimos los datos calculados: producción, estaciones, y RUNAP
    merged = base.merge(df_prod, on="MPIO_CCDGO", how="left")
    merged = merged.merge(df_est, on="MPIO_CCDGO", how="left")
    merged = merged.merge(df_runap, on="MPIO_CCDGO", how="left")

    # Rellenamos vacíos con ceros
    for col in ["area_ha", "produccion_t", "rendimiento_t_ha", "num_estaciones", "area_runap_m2"]:
        if col in merged.columns:
            merged[col] = merged[col].fillna(0)

    # Normalizamos cada variable para que estén en la misma escala (0 a 1)
    for col in ["produccion_t", "num_estaciones", "area_runap_m2"]:
        max_val = merged[col].max()
        merged[f"norm_{col}"] = merged[col] / max_val if max_val else 0

    # Calculamos un puntaje compuesto con pesos: 80% producción, 15% estaciones, 5% áreas protegidas
    merged["SCORE"] = (
        0.8 * merged["norm_produccion_t"] +
        0.15 * merged["norm_num_estaciones"] +
        0.05 * merged["norm_area_runap_m2"]
    )

    print("✅ SCORE calculado")
    return merged.sort_values("SCORE", ascending=False)


# In[8]:


# --- FUNCIONES DE EJECUCIÓN ---
def procesar_datos_completos():
    rutas = definir_rutas()
    gdf_mun, eva, gdf_est, gdf_runap = cargar_datos(rutas)
    
    df_prod = calcular_produccion_avocado(eva)
    df_est = contar_estaciones_activas(gdf_est, gdf_mun)
    df_runap = evaluar_superposicion_runap(gdf_runap, gdf_mun)
    df_score = calcular_score_final(gdf_mun, df_prod, df_est, df_runap)

    df_score["has_runap"] = df_score["area_runap_m2"] > 0

    top_validos = df_score[df_score["produccion_t"] > 0].sort_values("SCORE", ascending=False).head(10)

    return df_score, top_validos


def filtrar_municipios_por_codigo(df_score, codigos):
    codigos = [str(c).zfill(5) for c in codigos]
    return df_score[df_score["MPIO_CCDGO"].isin(codigos)]




