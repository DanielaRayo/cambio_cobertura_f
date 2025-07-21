# --- Funciones para clustering temporal con Earth Engine ---

def sample_training_data(vertex_stack, aoi, scale=60, num_pixels=5000):
    """
    Muestra datos desde los rasters de vértices para entrenamiento.
    """
    region = aoi.geometry().bounds()

    return vertex_stack.sample(
        region=region,         
        scale=scale,
        numPixels=num_pixels,
        seed=42
    )



def entrenar_kmeans(training_data, num_clusters=10):
    """Entrena un cluster k-means con Weka."""
    return ee.Clusterer.wekaKMeans(num_clusters).train(training_data)

def aplicar_clustering(vertex_stack, clusterer, num_clusters=10):
    """Aplica el modelo entrenado a todos los píxeles."""
    resultado = vertex_stack.cluster(clusterer)
    # Remapea clase 0 a 10 si deseas evitar el valor 0
    return resultado.remap(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    ).rename('cluster')
