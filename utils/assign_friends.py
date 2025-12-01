import random
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.supabase_client import get_supabase_client

# Load environment variables
load_dotenv()

def fetch_user_ids(supabase):
    """Obtener todos los IDs de los usuarios de la tabla users."""
    try:
        response = supabase.table('users').select('id').execute()
        if response.data:
            return [row['id'] for row in response.data]
        return []
    except Exception as e:
        print(f"Error al obtener los IDs de usuarios: {e}")
        return []

def assign_secret_friends(user_ids):
    """
    Asignar un amigo secreto a cada usuario.
    Garantiza que nadie se asigne a sí mismo.
    """
    if len(user_ids) < 2:
        print("No hay suficientes usuarios para realizar el sorteo.")
        return []
        
    assigned_ids = user_ids[:]
    while True:
        random.shuffle(assigned_ids)  # Mezclar aleatoriamente
        # Verificar que ningún usuario sea su propio amigo secreto
        if all(user_id != assigned_id for user_id, assigned_id in zip(user_ids, assigned_ids)):
            break
    
    # Create list of dictionaries for Supabase insert
    assignments = [
        {"user_id": uid, "id_secret_friend": aid} 
        for uid, aid in zip(user_ids, assigned_ids)
    ]
    return assignments

def save_assignments_to_db(supabase, assignments):
    """
    Guardar las asignaciones de amigo secreto en la tabla secret_friends.
    """
    try:
        # Limpiar la tabla antes de insertar nuevos datos
        # Delete all rows where user_id is greater than -1 (effectively all rows)
        supabase.table('secret_friends').delete().gt('user_id', -1).execute()
        
        # Insertar asignaciones
        if assignments:
            response = supabase.table('secret_friends').insert(assignments).execute()
            if response.data:
                print("Asignaciones de amigo secreto guardadas exitosamente.")
            else:
                print("No se pudieron guardar las asignaciones.")
    except Exception as e:
        print(f"Error al guardar las asignaciones en la base de datos: {e}")

def main():
    # Get Supabase client
    try:
        supabase = get_supabase_client()
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return

    # Obtener los IDs de los usuarios
    user_ids = fetch_user_ids(supabase)
    if not user_ids:
        print("No se encontraron usuarios en la base de datos.")
        return

    # Asignar amigos secretos
    assignments = assign_secret_friends(user_ids)

    # Guardar las asignaciones en la base de datos
    if assignments:
        save_assignments_to_db(supabase, assignments)

if __name__ == "__main__":
    main()