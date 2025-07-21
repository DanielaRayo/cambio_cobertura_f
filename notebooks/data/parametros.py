# --- Parámetros generales del análisis ---

# ID del asset de Earth Engine que representa el Área de Interés (AOI)
aoi_asset_id = "projects/ee-mismapasgee/assets/Palmira"

# Paleta de colores para representar clases de uso/cobertura del suelo MODIS (LC_Type1)
# Cada color representa una clase distinta, como bosque, agricultura, urbano, etc.
modis_palette = [
    '05450a', '086a10', '54a708', '78d203', '009900',   # verdes (bosques, vegetación)
    'c6b044', 'dcd159', 'dade48',                       # pastos, cultivos
    'fbff13', 'b6ff05', '27ff87',                       # agricultura
    'c24f44', 'a5a5a5', 'ff6d4c',                       # áreas urbanas, sin vegetación
    '69fff8', 'f9ffa4', '1c0dff'                        # agua, nieve, etc.
]

# Paleta de colores para representar datos climáticos 
wc_palette = [
    '006400',  # bosque denso
    'ffbb22',  # sabana
    'ffff4c',  # tierras agrícolas
    'f096ff',  # áreas húmedas
    'fa0000',  # áreas degradadas o urbanas
    'b4b4b4', 'f0f0f0',  # zonas sin datos o con baja cobertura
    '0032c8', '0096a0', '00cf75',  # agua o vegetación muy densa
    'fae6a0'  # zonas áridas o secas
]

# Lista de años que se van a analizar (de 2001 a 2020 inclusive)
years = list(range(2001, 2021))  # Equivalente a: [2001, 2002, ..., 2020]


