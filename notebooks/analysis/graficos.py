# --- Función para graficar NDVI vs Precipitación normalizados ---
def graficar_ndvi_vs_precipitacion(df):
    # Elimina filas con valores nulos en las columnas clave
    df = df.dropna(subset=['NDVI_promedio', 'Precipitacion_mm'])

    # Normaliza NDVI entre 0 y 1
    df['NDVI_norm'] = (df['NDVI_promedio'] - df['NDVI_promedio'].min()) / (df['NDVI_promedio'].max() - df['NDVI_promedio'].min())
    
    # Normaliza Precipitación entre 0 y 1
    df['Precip_norm'] = (df['Precipitacion_mm'] - df['Precipitacion_mm'].min()) / (df['Precipitacion_mm'].max() - df['Precipitacion_mm'].min())

    # Crea figura y eje para el gráfico
    fig, ax = plt.subplots(figsize=(14, 6))

    # Dibuja las curvas normalizadas
    ax.plot(df['Año'], df['NDVI_norm'], 'g-o', label='NDVI (normalizado)', linewidth=2)         # Línea verde con puntos
    ax.plot(df['Año'], df['Precip_norm'], 'b-s', label='Precipitación (normalizada)', linewidth=2)  # Línea azul con cuadrados

    # Añade etiquetas con valores originales sobre cada punto
    for i in range(len(df)):
        ax.text(df['Año'].iloc[i], df['NDVI_norm'].iloc[i] + 0.02, f"{df['NDVI_promedio'].iloc[i]:.2f}", color='green', ha='center', fontsize=8)
        ax.text(df['Año'].iloc[i], df['Precip_norm'].iloc[i] - 0.04, f"{int(df['Precipitacion_mm'].iloc[i])}", color='blue', ha='center', fontsize=8)

    # Configura etiquetas del eje y título
    ax.set_ylabel("Valores normalizados (0–1)")
    ax.set_title("NDVI vs Precipitación (valores normalizados)")
    
    # Configura eje X con años y formato
    ax.set_xticks(df['Año'])
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # Muestra leyenda y ajusta diseño
    ax.legend()
    plt.tight_layout()
    plt.show()
    
# --- Función para obtener el rango (mínimo y máximo) de cada banda 'fittedResidual' en los años seleccionados ---
def obtener_rango_fitted(fitted_stack, years, aoi):
    import ee
    rangos = {}
    for year in years:
        banda = fitted_stack.select(f'fittedResidual_{year}')  # Selecciona la banda correspondiente al año
        stats = banda.reduceRegion(
            reducer=ee.Reducer.minMax(),                       # Calcula mínimo y máximo
            geometry=aoi.geometry(),                           # Dentro del área de interés
            scale=250,                                         # Resolución de 250 metros
            maxPixels=1e13                                     # Límite de píxeles para evitar errores
        ).getInfo()
        rangos[year] = (
            stats.get(f'fittedResidual_{year}_min'),           # Guarda el mínimo
            stats.get(f'fittedResidual_{year}_max')            # Guarda el máximo
        )
    return rangos  # Devuelve un diccionario con los rangos por año

# --- Función para mostrar los mapas 'fitted' de NDVI ajustado por año usando Matplotlib ---
def mostrar_landtrendr_fitted(fitted_stack, years, aoi, palette=None, rangos=None):
    import matplotlib.pyplot as plt
    from utils.display import mostrar_imagen_ee  # Función personalizada para mostrar imágenes de EE

    # Crea una figura con subplots, uno por cada año
    fig, axes = plt.subplots(1, len(years), figsize=(6 * len(years), 5))

    # Itera por cada año a mostrar
    for i, year in enumerate(years):
        banda = fitted_stack.select(f'fittedResidual_{year}')  # Selecciona la banda para ese año
        
        # Usa rangos personalizados si están definidos, si no usa un rango por defecto
        if rangos and year in rangos:
            min_val = float(rangos[year]['min'])
            max_val = float(rangos[year]['max'])
        else:
            min_val, max_val = -0.2, 0.8

        # Visualiza la imagen con los parámetros definidos
        mostrar_imagen_ee(
            imagen=banda,
            region=aoi,
            titulo=f'Fitted NDVI {year}',           # Título específico para el año
            min_val=min_val,
            max_val=max_val,
            palette=palette or ["ff0000", "ffffff", "00ff00"],  # Paleta por defecto: rojo-blanco-verde
            ax=axes[i],                             # Dibuja en el subplot correspondiente
            barra_color=False                       # No mostrar barra de color
        )

    plt.tight_layout()  # Ajusta espaciado
    plt.show()          # Muestra el conjunto de mapas
