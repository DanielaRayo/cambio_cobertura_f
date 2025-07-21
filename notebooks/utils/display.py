# --- Función para mostrar una imagen de Earth Engine con matplotlib ---
def mostrar_imagen_ee(imagen, region, titulo="Imagen EE", min_val=0, max_val=255, palette=None, dimensiones=512, formato="png", ax=None, barra_color=True):
    # Si la región es una colección de features, se obtiene la geometría directamente
    if isinstance(region, ee.FeatureCollection):
        region = region.geometry()

    # Solicita una URL de miniatura para la imagen desde EE
    url = imagen.getThumbURL({
        'region': region.bounds(),      # Región a visualizar
        'dimensions': dimensiones,      # Tamaño de la imagen (píxeles)
        'format': formato,              # Formato de imagen (por defecto PNG)
        'min': min_val,                 # Valor mínimo para la visualización
        'max': max_val,                 # Valor máximo para la visualización
        'palette': palette or ['000000', 'FFFFFF']  # Paleta de color por defecto
    })

    # Descarga la imagen desde la URL
    response = requests.get(url)

    # Si la imagen no se generó correctamente, se avisa y no se muestra
    if len(response.content) < 1000:
        print(f"No se obtuvo imagen válida desde Earth Engine, se omite: {titulo}")
        return

    # Convierte la respuesta a imagen
    img = Image.open(BytesIO(response.content))

    # Si no se proporcionó un eje, se crea una nueva figura y eje
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(img)  # Muestra la imagen
        ax.set_title(titulo, fontsize=14)
        ax.axis("off")  # Oculta los ejes

        # Si se quiere mostrar la barra de color y hay paleta
        if palette and barra_color:
            cmap = mcolors.ListedColormap([f"#{c}" for c in palette])  # Crea mapa de colores
            norm = mcolors.Normalize(vmin=min_val, vmax=max_val)       # Normaliza rango
            cax = fig.add_axes([0.85, 0.15, 0.03, 0.7])                 # Posición de la barra de color
            ColorbarBase(ax=cax, cmap=cmap, norm=norm, orientation='vertical')
            cax.set_ylabel('Valores (escala relativa)', fontsize=10)

        # Ajuste final de la figura
        fig.subplots_adjust(left=0.05, right=0.8, top=0.90, bottom=0.05)
        plt.show()
    else:
        # Si ya se proporcionó un eje, se usa ese para dibujar
        ax.imshow(img)
        ax.set_title(titulo, fontsize=12)
        ax.axis("off")

# --- Función para obtener rangos (mínimo y máximo) de los fitted por año ---
def obtener_rango_fitted(fitted_stack, years, aoi):
    import ee
    rangos = {}

    # Si el AOI es un FeatureCollection, se obtiene su geometría
    if isinstance(aoi, ee.FeatureCollection):
        aoi = aoi.geometry()

    for year in years:
        banda = f"fittedResidual_{year}"  # Nombre de la banda del año correspondiente

        # Reduce la región para obtener valores mínimo y máximo
        stats = fitted_stack.select(banda).reduceRegion(
            reducer=ee.Reducer.minMax(),  # Calcula min y max
            geometry=aoi,                 # Sobre el área de interés
            scale=250,                    # Escala de resolución (250m)
            bestEffort=True               # Ajusta automáticamente si hay muchos píxeles
        ).getInfo()

        # Intenta convertir los valores; si falla, usa valores por defecto
        try:
            min_val = float(stats.get(f"{banda}_min", -0.2))
            max_val = float(stats.get(f"{banda}_max", 0.8))
        except Exception as e:
            print(f"⚠️ Error en año {year}: {e}")
            min_val, max_val = -0.2, 0.8

        # Guarda los rangos en un diccionario por año
        rangos[year] = {"min": min_val, "max": max_val}

    return rangos  # Devuelve un diccionario con los rangos para cada año

# --- Función para mostrar varias imágenes fitted (una por año) ---
def mostrar_landtrendr_fitted(fitted_stack, years, aoi, palette=None, rangos=None):
    import matplotlib.pyplot as plt
    from utils.display import mostrar_imagen_ee

    # Crea una figura con subplots horizontales, uno por cada año
    fig, axes = plt.subplots(1, len(years), figsize=(6 * len(years), 5))

    for i, year in enumerate(years):
        banda = fitted_stack.select(f'fittedResidual_{year}')  # Selecciona la banda del año actual

        # Usa el rango si está definido, si no usa valores por defecto
        rango = rangos.get(year, {"min": -0.2, "max": 0.8}) if rangos else {"min": -0.2, "max": 0.8}

        # Muestra la imagen ajustada para ese año
        mostrar_imagen_ee(
            imagen=banda,
            region=aoi,
            titulo=f'Fitted NDVI {year}',
            min_val=rango["min"],
            max_val=rango["max"],
            palette=palette or ["ff0000", "ffffff", "00ff00"],  # Paleta por defecto: rojo-blanco-verde
            ax=axes[i],
            barra_color=False  # No mostrar barra de color en este caso
        )

    plt.tight_layout()
    plt.show()  # Muestra todas las imágenes juntas

# --- Función para mostrar una imagen de clustering como imagen estática ---
def mostrar_clustering(imagen_cluster, region, titulo="Clustering", palette=None):
    """
    Muestra el raster de clustering como imagen estática con matplotlib.
    """
    mostrar_imagen_ee(
        imagen=imagen_cluster,
        region=region,
        titulo=titulo,
        min_val=0,
        max_val=9,  # Rango de clases esperadas (si se usaron 10 clusters: 0 a 9)
        palette=palette or [  # Paleta por defecto de 10 colores distintos
            "e6194b", "3cb44b", "ffe119", "4363d8", "f58231",
            "911eb4", "46f0f0", "f032e6", "bcf60c", "fabebe"
        ]
    )

