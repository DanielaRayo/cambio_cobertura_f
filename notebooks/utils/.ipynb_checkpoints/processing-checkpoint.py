import ee

def annual_precip(year, aoi):
    start = ee.Date.fromYMD(year, 1, 1)
    end = start.advance(1, 'year')
    precip = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY').filterDate(start, end).filterBounds(aoi).select('precipitation')
    return ee.Image(ee.Algorithms.If(
        precip.size().gt(0),
        precip.sum().rename('precip').clip(aoi).set({'year': year, 'system:time_start': start.millis()}),
        ee.Image().set({'year': year, 'empty': True})
    ))

def annual_max_ndvi(year, aoi):
    start = ee.Date.fromYMD(year, 1, 1)
    end = start.advance(1, 'year')
    ndvi = ee.ImageCollection('MODIS/061/MOD13Q1').filterDate(start, end).filterBounds(aoi).select('NDVI')
    return ee.Image(ee.Algorithms.If(
        ndvi.size().gt(0),
        ndvi.max().multiply(0.0001).rename('greenness').clip(aoi).set({'year': year, 'system:time_start': start.millis()}),
        ee.Image().set({'year': year, 'empty': True})
    ))

def combinar_ndvi_precip(year, aoi):
    ndvi = annual_max_ndvi(year, aoi)  # devuelve banda 'greenness'
    precip = annual_precip(year, aoi)  # devuelve banda 'precip'
    return ee.Image(ndvi).addBands(precip).set({
        'year': year,
        'system:time_start': ndvi.get('system:time_start')
    })



def ejecutar_landtrendr(collection, max_segments=6, spike_threshold=0.9, vertex_overshoot=3,
                        prevent_recovery=True, recovery_threshold=0.25, pval=0.05,
                        best_model_prop=0.75, min_obs=10):
    import ee
    params = {
        'maxSegments': max_segments,
        'spikeThreshold': spike_threshold,
        'vertexCountOvershoot': vertex_overshoot,
        'preventOneYearRecovery': prevent_recovery,
        'recoveryThreshold': recovery_threshold,
        'pvalThreshold': pval,
        'bestModelProportion': best_model_prop,
        'minObservationsNeeded': min_obs,
        'timeSeries': collection
    }
    lt = ee.Algorithms.TemporalSegmentation.LandTrendr(**params)
    return lt.select('LandTrendr')


def extraer_fitted_stack(lt_output, start_year, num_years):
    """
    A partir del resultado LandTrendr, extrae la banda 'fitted' y la aplana por año.
    Devuelve una imagen con una banda por año.
    """
    fitted = lt_output.arraySlice(0, 2, 3)
    year_labels = [str(start_year + i) for i in range(num_years)]
    return fitted.arrayFlatten([['fittedResidual'], year_labels]).toFloat()

import ee
import numpy as np
import pandas as pd

def calcular_residuos(imagenes, aoi):
    def extraer_valores(imagen):
        stats = imagen.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=aoi.geometry(),
            scale=250,
            maxPixels=1e13
        )
        return ee.Feature(None, {
            'greenness': stats.get('greenness'),
            'precip': stats.get('precip'),
            'year': ee.Date(imagen.get('system:time_start')).get('year')
        })

    # Ejecutar en Earth Engine y traer los datos
    features = imagenes.map(extraer_valores).getInfo()
    valores = []
    for f in features['features']:
        props = f['properties']
        if 'greenness' in props and 'precip' in props:
            valores.append({
                'ndvi': props['greenness'],
                'precip': props['precip'],
                'year': props['year']
            })

    df = pd.DataFrame(valores).dropna()

    if df.empty:
        raise ValueError("No hay datos válidos con 'greenness' y 'precip'.")

    x = df['precip'].values
    y = df['ndvi'].values
    pendiente, intercepto = np.polyfit(x, y, 1)

    def agregar_residual(imagen):
        predicho = imagen.expression(
            'b * p + a',
            {'p': imagen.select('precip'), 'a': intercepto, 'b': pendiente}
        ).rename('predicho')
        residual = imagen.select('greenness').subtract(predicho).rename('residual')
        return imagen.addBands(residual)

    return imagenes.map(agregar_residual)


