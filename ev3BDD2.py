from pymongo import MongoClient

# Conexión al servidor de MongoDB
client = MongoClient("localhost", 27017)

# Base de datos y colecciones
db = client.players
ranking = db.ranking
tournaments = db.tournaments

# Función para actualizar el ranking y los torneos
def actualizar_puntos_torneo(nombre_jugador, nombre_torneo, puntos_ganados):
    # Actualizar los puntos del jugador en la colección "ranking"
    ranking.update_one({"nombre": nombre_jugador}, {"$inc": {"points": puntos_ganados}})
    
    # Reordenar el ranking después de actualizar los puntos de un jugador
    reordenar_ranking()
    
    # Insertar al jugador en el torneo y registrar los puntos ganados
    tournaments.update_one({"nombre": nombre_torneo}, {"$set": {"jugadores." + nombre_jugador: puntos_ganados}}, upsert=True)

# Función para reordenar el ranking después de actualizar los puntos de un jugador
def reordenar_ranking():
    # Obtener todos los jugadores ordenados por puntos de mayor a menor
    jugadores_ordenados = ranking.find().sort("points", -1)
    
    # Actualizar el ranking para cada jugador
    for index, jugador in enumerate(jugadores_ordenados):
        nuevo_ranking = index + 1
        ranking.update_one({"_id": jugador["_id"]}, {"$set": {"ranking": nuevo_ranking}})

# Ejemplo de uso de la función
nombre_jugador = "Ricardo Perez"
nombre_torneo = "Table Tennis World Championship"
puntos_ganados = 700

actualizar_puntos_torneo(nombre_jugador, nombre_torneo, puntos_ganados)

# Mostrar el jugador actualizado en la colección "ranking"
print("Jugador actualizado:")
print(ranking.find_one({"nombre": nombre_jugador}))

# Mostrar el torneo actualizado
print("\nTorneo actualizado:")
print(tournaments.find_one({"nombre": nombre_torneo}))
