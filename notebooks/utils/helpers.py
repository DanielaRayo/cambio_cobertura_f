def listar_bandas(coleccion_id):
    # Obtiene la primera imagen de la colección especificada por ID
    img = ee.ImageCollection(coleccion_id).first()

    # Obtiene la lista de nombres de bandas de esa imagen
    bandas = img.bandNames()

    # Imprime las bandas disponibles en la colección
    print(f'Bandas de {coleccion_id}:')
    print(bandas.getInfo())  # getInfo() devuelve los datos como un diccionario de Python
    print('-' * 50)


def reproyectar_imagenes(coleccion, proyeccion):
    # Aplica reproyección a cada imagen de la colección usando la proyección proporcionada
    return coleccion.map(lambda img: img.reproject(proyeccion))

