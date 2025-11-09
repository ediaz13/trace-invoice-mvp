# api/index.py

# 1. Importamos la aplicación 'app' que definimos en main.py
from main import app
# 2. Importamos el adaptador Mangum
from mangum import Mangum

# 3. La instancia de Mangum envuelve la app de FastAPI
# Vercel ejecutará esta variable 'handler'
handler = Mangum(app)