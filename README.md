# 🛰️ Detección de Cambios en la Cobertura Terrestre de Pastizales

**Autor:** Daniela Rayo Álvarez  
**Programa:** Doctorado en Ciencias Agrarias  
**Facultad:** Facultad de Ciencias Agrarias  

## 🌍 Introducción

Los pastizales áridos y semiáridos cubren aproximadamente el 41% de la superficie terrestre. Estos ecosistemas son fundamentales para el sustento de millones de personas y para la actividad ganadera global. Sin embargo, enfrentan presiones crecientes debido al cambio climático, la expansión agrícola, la urbanización y la gestión inadecuada.

Las bases de datos satelitales tradicionales (como MODIS, GlobCover o WorldCover) presentan limitaciones de precisión en estas regiones y suelen detectar cambios solo cuando ya son evidentes. Herramientas como **LandTrendr**, que analizan series temporales de imágenes, permiten detectar cambios sutiles en la vegetación al identificar patrones en la trayectoria de los píxeles a lo largo del tiempo. Esto mejora la capacidad de monitoreo y análisis de la condición y resiliencia de los ecosistemas frente a perturbaciones climáticas o antrópicas.

## Objetivo

Detectar y analizar cambios en la cobertura vegetal de pastizales usando Google Earth Engine y técnicas de aprendizaje no supervisado, con énfasis en la segmentación temporal y el análisis de residuos.

## Estructura del Proyecto

```cc
notebooks/
│
├── analysis/                 # Gráficos y análisis visual
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
Desde `notebooks/auth/gee_auth.py` o cualquier celda:

### 2. Definir el Área de Estudio (AOI)
Se carga desde un *asset* de Earth Engine en `data/select_muni`.

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
Todo implementado con `matplotlib`.

## 🛠️ Tecnologías Utilizadas

- 🌐 Google Earth Engine
- 🛰️ MODIS MOD13Q1 NDVI
- 🌧️ CHIRPS precipitation data
- 🧠 LandTrendr (segmentación temporal)
- 📊 K-means clustering
- 🐍 Python: `pandas`, `numpy`, `matplotlib`

## 📚 Referencia Bibliográfica

Este proyecto se basa en una adaptación del capítulo:

> Palmer, A. R., & Fortescue, A. (2004). *Remote sensing and change detection in rangelands*.  
> _African Journal of Range and Forage Science, 21(2), 123–128._  
> [DOI:10.2989/10220110409485846](https://doi.org/10.2989/10220110409485846)
