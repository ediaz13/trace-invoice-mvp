# api/index.py

# Importamos la aplicación 'app' que definimos en main.py
from main import app
from vercel_python import VercelServer

# Creamos una instancia del servidor Vercel usando la aplicación FastAPI
server = VercelServer(app)