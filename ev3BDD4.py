from pymongo import MongoClient

# Conexión al servidor de MongoDB
client = MongoClient("localhost", 27017)

# Base de datos y colecciones
db = client.players
ranking = db.ranking
tournaments = db.tournaments

def mostrar_participaciones(nombre_jugador):
    filtro_jugador = {"jugadores." + nombre_jugador: {"$exists": True}}
    torneos_jugador = tournaments.find(filtro_jugador)
    
    print(f"\nParticipaciones de '{nombre_jugador}' en los torneos:")
    for torneo in torneos_jugador:
        print(torneo)


def buscar_ranking(nombre=None, puesto=None):
    filtros = {}
    if nombre:
        filtros["nombre"] = nombre
    if puesto:
        filtros["ranking"] = puesto
    
    resultados = ranking.find(filtros)
    
    primer_resultado = next(resultados, None)
    if primer_resultado is None:
        print("No se encontraron resultados.")
        return
    
    print("\nResultados de búsqueda en la colección 'ranking':")
    print(primer_resultado)
    
    opcion = input("¿Mostrar participaciones en torneos? (si/no): ")
    if opcion.lower() == "si":
        mostrar_participaciones(primer_resultado["nombre"])


def buscar_torneos(nombre=None, nombre_torneo=None):
    if nombre:
        filtro_jugador = {"jugadores." + nombre: {"$exists": True}}
        torneos_jugador = tournaments.find(filtro_jugador)
        
        print(f"\nResultados de búsqueda para el jugador '{nombre}' en la colección 'tournaments':")
        for torneo in torneos_jugador:
            print(torneo)
    elif nombre_torneo:
        filtros = {"nombre": nombre_torneo}
        resultados = tournaments.find(filtros)
        
        if resultados.count() == 0:
            print("No se encontraron resultados.")
        else:
            print("\nResultados de búsqueda en la colección 'tournaments':")
            for torneo in resultados:
                print(torneo)
    else:
        print("No se proporcionaron criterios de búsqueda.")


def realizar_busqueda():
    print("\n¿En qué colección desea buscar?")
    print("1. Ranking")
    print("2. Tournaments")
    opcion_coleccion = input("Seleccione una opción (1 o 2): ")
    
    if opcion_coleccion == "1":
        print("\n¿Qué desea buscar en el ranking?")
        print("1. Jugador")
        print("2. Posición en el ranking")
        opcion_busqueda = input("Seleccione una opción (1 o 2): ")
        
        if opcion_busqueda == "1":
            nombre_jugador = input("Ingrese el nombre del jugador: ")
            buscar_ranking(nombre=nombre_jugador)
        elif opcion_busqueda == "2":
            try:
                puesto = int(input("Ingrese el número en el ranking que desea buscar: "))
                buscar_ranking(puesto=puesto)
            except ValueError:
                print("Error: Por favor ingrese un número válido.")
        else:
            print("Opción inválida.")
    
    elif opcion_coleccion == "2":
        print("\n¿Qué desea buscar en los torneos?")
        print("1. Jugador")
        print("2. Torneo")
        opcion_busqueda = input("Seleccione una opción (1 o 2): ")
        
        if opcion_busqueda == "1":
            nombre_jugador = input("Ingrese el nombre del jugador: ")
            buscar_torneos(nombre=nombre_jugador)
        elif opcion_busqueda == "2":
            nombre_torneo = input("Ingrese el nombre del torneo: ")
            buscar_torneos(nombre_torneo=nombre_torneo)
        else:
            print("Opción inválida.")
    
    else:
        print("Opción inválida.")

# Ejecutar la búsqueda
realizar_busqueda()
