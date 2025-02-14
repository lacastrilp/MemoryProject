import os
import pandas as pd
import json

def cargar_archivos(carpeta):
    """Carga todos los archivos CSV y JSON de una carpeta en memoria con porcentaje de progreso."""
    if not os.path.isdir(carpeta):
        print(f"Error: La carpeta '{carpeta}' no existe.")
        return None, None, None, None

    usuarios = {}
    juegos = {}
    recomendaciones = []
    metadata = []

    archivos = os.listdir(carpeta)
    total_archivos = len(archivos)

    for idx, archivo in enumerate(archivos, start=1):
        ruta = os.path.join(carpeta, archivo)
        print(f"Cargando {archivo}... ({idx}/{total_archivos} - {((idx/total_archivos)*100):.2f}%)")

        try:
            if archivo.endswith("users.csv"):
                df = pd.read_csv(ruta)
                usuarios = {row.user_id: {"products": row.products, "reviews": row.reviews} for _, row in df.iterrows()}
            elif archivo.endswith("games.csv"):
                df = pd.read_csv(ruta)
                juegos = {row.app_id: {"title": row.title, "review_score": row.rating, "user_reviews": row.user_reviews}
                          for _, row in df.iterrows()}
            elif archivo.endswith("recommendations.csv"):
                df = pd.read_csv(ruta)
                recomendaciones = df.to_dict(orient="records")
            elif archivo.endswith("games_metadata.json"):
                with open(ruta, "r", encoding="utf-8") as f:
                    metadata = [json.loads(line) for line in f if line.strip()]
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")

    print("Archivos cargados correctamente en memoria.")
    return usuarios, juegos, recomendaciones, metadata

def mostrar_menu(usuarios, juegos, recomendaciones):
    print("Menú cargado...")
    while True:
        print("\nMenú de Opciones:")
        print("1. Mostrar los 10 juegos más recomendados")
        print("2. Mostrar los 10 juegos menos recomendados")
        print("3. Mostrar los 10 usuarios con más recomendaciones")
        print("4. Mostrar los juegos que más recomiendan los 10 usuarios principales")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            top_juegos = sorted(juegos.items(), key=lambda x: x[1]["user_reviews"], reverse=True)[:10]
            for app_id, info in top_juegos:
                print(f"{info['title']} - {info['user_reviews']} recomendaciones")
        elif opcion == "2":
            bottom_juegos = sorted(juegos.items(), key=lambda x: x[1]["user_reviews"])[:10]
            for app_id, info in bottom_juegos:
                print(f"{info['title']} - {info['user_reviews']} recomendaciones")
        elif opcion == "3":
            top_usuarios = sorted(usuarios.items(), key=lambda x: x[1]["reviews"], reverse=True)[:10]
            for user_id, info in top_usuarios:
                print(f"Usuario {user_id} - {info['reviews']} recomendaciones")
        elif opcion == "4":
            top_usuarios = sorted(usuarios.items(), key=lambda x: x[1]["reviews"], reverse=True)[:10]
            top_user_ids = {user_id for user_id, _ in top_usuarios}
            top_recommendations = [r for r in recomendaciones if r["user_id"] in top_user_ids]
            print("\nJuegos más recomendados por los 10 usuarios principales:")
            for r in top_recommendations[:10]:
                status = "✅ Recomendado" if r["is_recommended"] else "❌ No recomendado"
                print(f"- Juego ID: {r['app_id']} | Horas jugadas: {r['hours']} | Usuario: {r['user_id']} | {status}")
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente nuevamente.")

# Ejemplo de uso
carpeta_datos = "C:\\Users\\Alejo\\Documents\\archive"
usuarios, juegos, recomendaciones, metadata = cargar_archivos(carpeta_datos)

# Verificar si los datos fueron cargados
print(f"Usuarios cargados: {len(usuarios)}")
print(f"Juegos cargados: {len(juegos)}")
print(f"Recomendaciones cargadas: {len(recomendaciones)}")
print(f"Metadata cargada: {len(metadata)}")

print("Menú cargado...")
mostrar_menu(usuarios, juegos, recomendaciones)
