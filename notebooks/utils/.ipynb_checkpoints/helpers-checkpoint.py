import ee

def listar_bandas(coleccion_id):
    img = ee.ImageCollection(coleccion_id).first()
    bandas = img.bandNames()
    print(f'Bandas de {coleccion_id}:')
    print(bandas.getInfo())
    print('-' * 50)

def reproyectar_imagenes(coleccion, proyeccion):
    return coleccion.map(lambda img: img.reproject(proyeccion))
