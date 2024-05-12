from pymongo import MongoClient
from pymongo import ASCENDING

# Conexión al servidor de MongoDB
client = MongoClient("localhost", 27017)

# Base de datos y colección
db = client.players
ranking = db.ranking

# Crear índice en el campo "points"
ranking.create_index([("points", ASCENDING)])

# Función para actualizar el ranking
def actualizar_ranking():
    # Obtener todos los jugadores ordenados por puntos de mayor a menor
    jugadores_ordenados = ranking.find().sort("points", -1)
    
    # Actualizar el ranking para cada jugador
    for index, jugador in enumerate(jugadores_ordenados):
        nuevo_ranking = index + 1
        ranking.update_one({"_id": jugador["_id"]}, {"$set": {"ranking": nuevo_ranking}})

# Datos de los jugadores con su respectivo ranking y puntos
jugadores = [
    {"nombre": "Emilio Mazariegos", "points": 5432},
    {"nombre": "Ximena Chavez", "points": 4745},
    {"nombre": "Ricardo Perez", "points": 4666},
    {"nombre": "Enrique Gutierrez", "points": 4500},
    {"nombre": "Ramon Panes", "points": 4505},
    {"nombre": "Brandon Hernandez", "points": 3876},
    {"nombre": "Huberto Vallejo", "points": 3500},
    {"nombre": "Roberto Garcia", "points": 3499},
    {"nombre": "Erika Chapa", "points": 2999},
    {"nombre": "Carlos Soto", "points": 1001}
]

# Insertar jugadores en la colección "ranking"
ranking.insert_many(jugadores)

# Actualizar el ranking después de insertar los jugadores
actualizar_ranking()

# Mostrar los jugadores en la colección "ranking"
for jugador in ranking.find():
    print(jugador)
