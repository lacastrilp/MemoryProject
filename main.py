from pathlib import Path
import pandas as pd
import threading

usuarios, juegos, recomendaciones = {}, {}, []

def cargar_archivos(carpeta):
    global usuarios, juegos, recomendaciones
    carpeta = Path(carpeta)
    if not carpeta.is_dir():
        print(f"Error: La carpeta '{carpeta}' no existe.")
        return

    archivos = list(carpeta.glob("*.csv"))  # Filtrar solo archivos CSV

    for idx, archivo in enumerate(archivos, start=1):
        print(f"Cargando {archivo.name}... ({idx}/{len(archivos)} - {idx / len(archivos) * 100:.2f}%)")

        try:
            df = pd.read_csv(archivo)
            if "users.csv" in archivo.name:
                usuarios = df.set_index("user_id").to_dict(orient="index")
            elif "games.csv" in archivo.name:
                juegos = df.set_index("app_id").to_dict(orient="index")
            elif "recommendations.csv" in archivo.name:
                recomendaciones = df.to_dict(orient="records")
        except Exception as e:
            print(f"Error al procesar {archivo.name}: {e}")

    print("Archivos cargados correctamente en memoria.")

def mostrar_menu(carpeta):
    # Iniciar la carga de archivos en un hilo separado
    hilo_carga = threading.Thread(target=cargar_archivos, args=(carpeta,))
    hilo_carga.start()

    opciones = {
        "1": lambda: mostrar_top_juegos(True),
        "2": lambda: mostrar_top_juegos(False),
        "3": mostrar_top_usuarios,
        "4": mostrar_recomendaciones_top_usuarios,
        "5": exit
    }

    while True:
        print("\nMenú de Opciones:")
        print("1. Mostrar los 10 juegos más recomendados")
        print("2. Mostrar los 10 juegos menos recomendados")
        print("3. Mostrar los 10 usuarios con más recomendaciones")
        print("4. Mostrar los juegos que más recomiendan los 10 usuarios principales")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")
        opciones.get(opcion, lambda: print("Opción no válida, intente nuevamente."))()

def mostrar_top_juegos(mas_recomendados=True):
    if not juegos:
        print("Los datos de juegos aún no se han cargado.")
        return
    top_juegos = sorted(juegos.items(), key=lambda x: x[1]["user_reviews"], reverse=mas_recomendados)[:10]
    for app_id, info in top_juegos:
        print(f"{info['title']} - {info['user_reviews']} recomendaciones")

def mostrar_top_usuarios():
    if not usuarios:
        print("Los datos de usuarios aún no se han cargado.")
        return
    top_usuarios = sorted(usuarios.items(), key=lambda x: x[1]["reviews"], reverse=True)[:10]
    for user_id, info in top_usuarios:
        print(f"Usuario {user_id} - {info['reviews']} recomendaciones")

def mostrar_recomendaciones_top_usuarios():
    if not usuarios or not recomendaciones:
        print("Los datos de usuarios o recomendaciones aún no se han cargado.")
        return
    top_users = {user_id for user_id, _ in sorted(usuarios.items(), key=lambda x: x[1]["reviews"], reverse=True)[:10]}
    top_recommendations = [r for r in recomendaciones if r["user_id"] in top_users]

    print("\nJuegos más recomendados por los 10 usuarios principales:")
    for r in top_recommendations[:10]:
        status = "✅ Recomendado" if r["is_recommended"] else "❌ No recomendado"
        print(f"- Juego ID: {r['app_id']} | Horas jugadas: {r['hours']} | Usuario: {r['user_id']} | {status}")

# Ejemplo de uso
carpeta_datos = "C:\\Users\\Alejo\\Documents\\archive"
mostrar_menu(carpeta_datos)
