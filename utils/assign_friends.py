import psycopg2
from psycopg2 import Error
import random
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de conexión a la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'dbname': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', '5432')
}

def connect_to_db():
    """Establecer conexión con la base de datos."""
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except (Exception, Error) as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def fetch_user_ids(connection):
    """Obtener todos los IDs de los usuarios de la tabla users."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id FROM "secret-santa".users""")
            user_ids = [row[0] for row in cursor.fetchall()]
            return user_ids
    except (Exception, Error) as e:
        print(f"Error al obtener los IDs de usuarios: {e}")
        return []

def assign_secret_friends(user_ids):
    """
    Asignar un amigo secreto a cada usuario.
    Garantiza que nadie se asigne a sí mismo.
    """
    assigned_ids = user_ids[:]
    while True:
        random.shuffle(assigned_ids)  # Mezclar aleatoriamente
        # Verificar que ningún usuario sea su propio amigo secreto
        if all(user_id != assigned_id for user_id, assigned_id in zip(user_ids, assigned_ids)):
            break
    return list(zip(user_ids, assigned_ids))

def save_assignments_to_db(connection, assignments):
    """
    Guardar las asignaciones de amigo secreto en la tabla secret_friends.
    """
    try:
        with connection.cursor() as cursor:
            # Limpiar la tabla antes de insertar nuevos datos (opcional)
            cursor.execute("""TRUNCATE TABLE "secret-santa".secret_friends RESTART IDENTITY""")
            # Insertar asignaciones
            cursor.executemany("""
                INSERT INTO "secret-santa".secret_friends (user_id, id_secret_friend)
                VALUES (%s, %s)
            """, assignments)
            connection.commit()
            print("Asignaciones de amigo secreto guardadas exitosamente.")
    except (Exception, Error) as e:
        print(f"Error al guardar las asignaciones en la base de datos: {e}")

def main():
    # Conectar a la base de datos
    connection = connect_to_db()
    if not connection:
        return

    try:
        # Obtener los IDs de los usuarios
        user_ids = fetch_user_ids(connection)
        if not user_ids:
            print("No se encontraron usuarios en la base de datos.")
            return

        # Asignar amigos secretos
        assignments = assign_secret_friends(user_ids)

        # Guardar las asignaciones en la base de datos
        save_assignments_to_db(connection, assignments)
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()