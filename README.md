# Detección de Cambios en la Cobertura Terrestre Mediante Sensores Remotos

**Autor:** Daniela Rayo Álvarez  
**Programa:** Doctorado en Ciencias Agrarias  
**Facultad:** Facultad de Ciencias Agrarias  

## Introducción

Los pastizales áridos y semiáridos cubren aproximadamente el 41% de la superficie terrestre. Estos ecosistemas son fundamentales para el sustento de millones de personas y para la actividad ganadera global. Sin embargo, enfrentan presiones crecientes debido al cambio climático, la expansión agrícola, la urbanización y la gestión inadecuada.

Las bases de datos satelitales tradicionales (como MODIS, GlobCover o WorldCover) presentan limitaciones de precisión en estas regiones y suelen detectar cambios solo cuando ya son evidentes. Herramientas como **LandTrendr**, que analizan series temporales de imágenes, permiten detectar cambios sutiles en la vegetación al identificar patrones en la trayectoria de los píxeles a lo largo del tiempo. Esto mejora la capacidad de monitoreo y análisis de la condición y resiliencia de los ecosistemas frente a perturbaciones climáticas o antrópicas.

## Objetivo

Analizar cambios en la cobertura vegetal de pastizales usando Google Earth Engine y técnicas de aprendizaje no supervisado, con énfasis en la segmentación temporal y el análisis de residuos.

## Estructura 

```cc
notebooks/
│
├── analysis/                # Gráficos y análisis visual
├── auth/                    # Autenticación con Google Earth Engine
├── data/                    # Parámetros, selección de AOI y variables
├── utils/                   # Funciones auxiliares
│   ├── clustering.py        # Agrupamiento K-means
│   ├── display.py           # Visualización de mapas e imágenes
│   ├── helpers.py           # Funciones generales
│   └── processing.py        # Preprocesamiento de datos
│
├── main.ipynb               # Script principal que organiza todo el flujo
```

```cc
documentos/                  # Documentos complementarios (PDFs, informes)
slides/                      # Presentación del proyecto (diapositivas)
```

##  ¿Cómo se ejecuta?

### 1. Autenticación en Earth Engine
Desde `notebooks/auth/gee_auth.py.

### 2. Definir el Área de Estudio (AOI)
Se carga desde un *asset* de Earth Engine en `data/parametros`.

### 3. Preprocesamiento
- Se calcula el **NDVI máximo anual** y la **precipitación acumulada anual**.
- Se ajusta una regresión lineal NDVI ~ Precipitación.
- Se calculan **residuos** (diferencia entre el NDVI observado y el esperado).

### 4. Segmentación Temporal
Se aplica **LandTrendr** a la serie temporal de residuos para identificar patrones de cambio no explicados por el clima.

### 5. Clustering K-means
Se agrupan los píxeles por similitud en la forma de sus series temporales de residuos.

### 6. Visualización de Resultados
- Mapas anuales
- Mapas de clustering
- Gráficos explicativos  

##  Tecnologías utilizadas

- Google Earth Engine
- MODIS MOD13Q1 NDVI
- CHIRPS precipitation data
- LandTrendr (segmentación temporal)
- K-means clustering
- Python

## Referencia

Este proyecto se inspira en el capítulo **A3.8: Detecting Land Cover Change in Rangelands**, el cual forma parte del libro:

> Cardille, J. A., Crowley, M. A., Saah, D., & Clinton, N. E. (Eds.). (2023).  
> *Cloud-based Remote Sensing with Google Earth Engine: Fundamentals and Applications*.  
> Springer Nature.

El capítulo aborda el uso de Earth Engine para detectar cambios sutiles en la cobertura de los pastizales mediante análisis de series temporales, lo cual sirve como base conceptual y técnica para el presente trabajo.
