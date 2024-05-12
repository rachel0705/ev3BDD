from pymongo import MongoClient

client = MongoClient("localhost", 27017)

#Se permite eliminar documentos de la colección 2, dejando el campo de relación vacío 
#para los documentos de la colección 1 que se relacionaban con el documento eliminado.


db = client.players
ranking = db.ranking
tournaments = db.tournaments

def eliminar_tournament():
    mostrar_torneos()
    nombre_torneo = input("Ingrese el nombre del torneo que desea eliminar: ")
    
    # Verificar si el torneo existe
    torneo = tournaments.find_one({"nombre": nombre_torneo})
    if not torneo:
        print("El torneo especificado no existe.")
        return
    
    # Eliminar el torneo - tournaments
    tournaments.delete_one({"nombre": nombre_torneo})
    
    # Eliminar puntos en ranking y recalculo
    for jugador, puntos in torneo["jugadores"].items():
        ranking.update_one({"nombre": jugador}, {"$inc": {"points": -puntos}})
    recalcular_ranking()
    
    print(f"El torneo '{nombre_torneo}' ha sido eliminado y los puntos de los jugadores han sido actualizados.")

def recalcular_ranking():
    # Verificacion de puntos
    jugadores_ordenados = list(ranking.find({"ranking": {"$ne": None}}).sort("points", -1))
    # Actualizar la posición de cada player en ranking
    for i, jugador in enumerate(jugadores_ordenados):
        ranking.update_one({"_id": jugador["_id"]}, {"$set": {"ranking": i+1}})
    print("Se ha recalculado el ranking basado en la información actualizada.")

def mostrar_torneos():
    print("Torneos disponibles:")
    for torneo in tournaments.find({}, {"nombre": 1}):
        print(torneo["nombre"])

def main():
    opcion = input("¿Desea eliminar un torneo? (si/no): ")
    if opcion.lower() == "s":
        eliminar_tournament()

if __name__ == "__main__":
    main()
