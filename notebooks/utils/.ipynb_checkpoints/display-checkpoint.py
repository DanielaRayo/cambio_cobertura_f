import ee
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colorbar import ColorbarBase
import requests
from PIL import Image
from io import BytesIO

def mostrar_imagen_ee(imagen, region, titulo="Imagen EE", min_val=0, max_val=255, palette=None, dimensiones=512, formato="png", ax=None, barra_color=True):
    if isinstance(region, ee.FeatureCollection):
        region = region.geometry()

    url = imagen.getThumbURL({
        'region': region.bounds(),
        'dimensions': dimensiones,
        'format': formato,
        'min': min_val,
        'max': max_val,
        'palette': palette or ['000000', 'FFFFFF']
    })

    response = requests.get(url)
    if len(response.content) < 1000:
        print(f"No se obtuvo imagen válida desde Earth Engine, se omite: {titulo}")
        return

    img = Image.open(BytesIO(response.content))

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(img)
        ax.set_title(titulo, fontsize=14)
        ax.axis("off")

        if palette and barra_color:
            cmap = mcolors.ListedColormap([f"#{c}" for c in palette])
            norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
            cax = fig.add_axes([0.85, 0.15, 0.03, 0.7])
            ColorbarBase(ax=cax, cmap=cmap, norm=norm, orientation='vertical')
            cax.set_ylabel('Valores (escala relativa)', fontsize=10)

        fig.subplots_adjust(left=0.05, right=0.8, top=0.90, bottom=0.05)
        plt.show()
    else:
        ax.imshow(img)
        ax.set_title(titulo, fontsize=12)
        ax.axis("off")

def obtener_rango_fitted(fitted_stack, years, aoi):
    """
    Calcula los valores mínimo y máximo de cada banda 'fittedResidual_YEAR' en la región dada.

    Args:
        fitted_stack (ee.Image): Imagen con bandas 'fittedResidual_YYYY'
        years (list of str): Lista de años como strings (ej. ['2005', '2010'])
        aoi (ee.Geometry or ee.FeatureCollection): Región para hacer el cálculo

    Returns:
        dict: Diccionario con los rangos para cada año:
              { '2005': {'min': -0.1, 'max': 0.15}, ... }
    """
    import ee
    rangos = {}

    if isinstance(aoi, ee.FeatureCollection):
        aoi = aoi.geometry()

    for year in years:
        banda = f"fittedResidual_{year}"
        stats = fitted_stack.select(banda).reduceRegion(
            reducer=ee.Reducer.minMax(),
            geometry=aoi,
            scale=250,
            bestEffort=True
        ).getInfo()

        if stats:
            rangos[year] = {
                "min": stats.get(f"{banda}_min", 0),
                "max": stats.get(f"{banda}_max", 1)
            }
        else:
            print(f"⚠️ No se pudo calcular el rango para {banda}")
            rangos[year] = {"min": 0, "max": 1}

    return rangos
