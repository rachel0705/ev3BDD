from pymongo import MongoClient
from bson.objectid import ObjectId

# Conexión al servidor de MongoDB
client = MongoClient("localhost", 27017)

# Base de datos y colección "tournaments"
db = client.players
tournaments = db.tournaments

# Datos de los torneos con sus IDs únicos
torneos = [
    {"_id": ObjectId(), "nombre": "Table Tennis International Tournament"},
    {"_id": ObjectId(), "nombre": "Table Tennis World Championship"},
    {"_id": ObjectId(), "nombre": "Table Tennis 1st Class"},
    {"_id": ObjectId(), "nombre": "Table Tennis Rocket League"},
    {"_id": ObjectId(), "nombre": "Table Tennis SINGAPORE"},
    {"_id": ObjectId(), "nombre": "Table Tennis Yearly Competition"}
]

# Insertar torneos en la colección "tournaments"
tournaments.insert_many(torneos)

# Mostrar los torneos insertados con sus IDs
print("Torneos insertados:")
for torneo in tournaments.find():
    print("- Nombre:", torneo["nombre"], "| ID:", torneo["_id"])
