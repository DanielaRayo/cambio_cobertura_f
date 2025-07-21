# --- Autenticación con Google Earth Engine (GEE) ---

# Función para autenticar y/o inicializar el entorno de GEE
def autenticar_gee():
    try:
        # Intenta inicializar GEE (si ya fue autenticado previamente, esto funciona directo)
        ee.Initialize()
        print("✅ Earth Engine ya estaba inicializado.")
    except Exception:
        # Si ocurre un error, probablemente no está autenticado
        print("🔐 Iniciando autenticación con Google Earth Engine...")

        # Abre el flujo de autenticación en modo notebook (apto para notebooks interactivos como Jupyter)
        ee.Authenticate(auth_mode='notebook')

        # Inicializa Earth Engine una vez autenticado
        ee.Initialize()
        print("✅ Autenticación e inicialización completadas.")
