from pymongo import MongoClient

client = MongoClient("localhost", 27017)

#Se permite realizar la actualización de ambas colecciones afectando la relación entre ellas.

db = client.players
ranking = db.ranking
tournaments = db.tournaments

#muestra las opciones a elejir ya disponibles en ranking, solo jugadores ya agregados
def mostrar_jugadores():
    print("\nJugadores en la colección 'ranking':")
    for jugador in ranking.find():
        print(jugador["nombre"])

#torneos ya agregados para escoger
def mostrar_torneos():
    print("\nTorneos disponibles en la colección 'tournaments':")
    for torneo in tournaments.find():
        print(torneo["nombre"])

#opcion 1 es para agregar un nuevo player a la coleccion, pide la info y actualiza el ranking
def agregar_jugador():
    nombre = input("Ingrese el nombre del jugador que desea agregar: ")
    nuevo_jugador = {
        "nombre": nombre,
        "ranking": None,
        "points": 0
    }
    ranking.insert_one(nuevo_jugador)
    print(f"El jugador '{nombre}' ha sido agregado a la colección 'ranking'.")

#cuando agregas un nuevo player tienes que poner en donde jugó (torneo), y sus respectivos points ganados
def actualizar_torneo(jugador):
    mostrar_torneos()
    torneo = input("Elija el nombre del torneo en el que participó el jugador (o 'salir' para terminar): ")
    if torneo == "salir":
        return
    puntos = int(input(f"Ingrese los puntos ganados por '{jugador}' en el torneo '{torneo}': "))
    
    #se actualizan los puntos en la colección 'tournaments'
    tournaments.update_one({"nombre": torneo}, {"$set": {"jugadores." + jugador: puntos}}, upsert=True)
    
    #se actualizan los puntos en la colección 'ranking'
    ranking.update_one({"nombre": jugador}, {"$inc": {"points": puntos}})
    print(f"Se han actualizado los puntos de '{jugador}' en el torneo '{torneo}'.")
    
    #se checa la info a actualizar 
    recalcular_ranking()
    mostrar_posicion(jugador)

#con los nuevos puntos se recalcula el ranking para que cada player tenga su posicion correcta
def recalcular_ranking():
    jugadores_ordenados = list(ranking.find({"ranking": {"$ne": None}}).sort("points", -1))
    for i, jugador in enumerate(jugadores_ordenados):
        ranking.update_one({"_id": jugador["_id"]}, {"$set": {"ranking": i+1}})
    print("Se ha recalculado el ranking.")

#se imprime la nueva info para ver la actualizacion
def mostrar_posicion(jugador):
    jugador_info = ranking.find_one({"nombre": jugador})
    print(f"\n'{jugador}' ahora se encuentra en la posición {jugador_info['ranking']} del ranking con {jugador_info['points']} puntos.")

#opcion para hacer otra adicion o salir
def actualizar_informacion():
    mostrar_jugadores()
    jugador = input("Seleccione el nombre del jugador al que desea actualizar la información (o 'salir' para terminar): ")
    if jugador == "salir":
        return
    actualizar_torneo(jugador)
    while True:
        continuar = input("¿Desea agregar más puntos para este jugador en otro torneo? (si/no): ")
        if continuar.lower() != "si":
            break
        actualizar_torneo(jugador)

#empieza la actualizacion de la informacion en la base de datos ya hecha
def main():
    while True:
        print("\n¿Qué acción desea realizar?")
        print("1. Agregar nuevo jugador a la colección 'ranking'")
        print("2. Actualizar información de un jugador en la colección 'ranking'")
        print("3. Salir")
        opcion = input("Seleccione una opción (1, 2 o 3): ")

        if opcion == "1":
            agregar_jugador()
        elif opcion == "2":
            actualizar_informacion()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
