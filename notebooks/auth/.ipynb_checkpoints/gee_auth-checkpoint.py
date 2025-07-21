import ee

def autenticar_gee():
    try:
        ee.Initialize()
        print("✅ Earth Engine ya estaba inicializado.")
    except Exception:
        print("🔐 Iniciando autenticación con Google Earth Engine...")
        ee.Authenticate(auth_mode='notebook')
        ee.Initialize()
        print("✅ Autenticación e inicialización completadas.")