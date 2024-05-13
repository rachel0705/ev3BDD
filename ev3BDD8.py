from pymongo import MongoClient

client = MongoClient("localhost", 27017)

#Se permite eliminar documentos de la colección 2, dejando el campo de relación vacío 
#para los documentos de la colección 1 que se relacionaban con el documento eliminado.

db = client.players
ranking = db.ranking
tournaments = db.tournaments

#recibe indicacion del torneo a eliminar, checa si existe y borra los puntos tanto de tournaments como de ranking
def eliminar_torneo(nombre_torneo):
    torneo = tournaments.find_one({"nombre": nombre_torneo})
    if torneo:
        jugadores = torneo.get("jugadores", {})
        tournaments.delete_one({"nombre": nombre_torneo})
        
        #recalcula la info, con los puntos borrados en tournament se actualiza el ranking
        for jugador, puntos in jugadores.items():
            ranking.update_one({"nombre": jugador}, {"$inc": {"points": -puntos}})
        
        print(f"El torneo '{nombre_torneo}' ha sido eliminado correctamente.")
    else:
        print("No se encontró el torneo especificado.")

#se elije eliminar un torneo
def menu_eliminar_torneo():
    print("Seleccione el torneo que desea eliminar:")
    
    #muestra la base de datos de los torneos ya registrados
    for torneo in tournaments.find():
        print(torneo["nombre"])
    nombre_torneo = input("Ingrese el nombre del torneo: ")
    eliminar_torneo(nombre_torneo)

menu_eliminar_torneo()
