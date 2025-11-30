import streamlit as st
import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv
import subprocess

# Load environment variables
load_dotenv()


class AdminPage:
    def __init__(self):
        # Database connection configuration
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'dbname': os.getenv('DB_NAME'),
            'port': os.getenv('DB_PORT', '5432')
        }

        # CSS para estilos personalizados
        st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
        }
        .stButton > button {
            color: white;
            background-color: #4CAF50;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .admin-button {
            background-color: #FF6B6B !important;
        }
        .admin-button:hover {
            background-color: #FF5252 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    def connect_to_db(self):
        """Establish a database connection."""
        try:
            connection = psycopg2.connect(**self.db_config)
            return connection
        except (Exception, Error) as e:
            st.error(f"Error connecting to the PostgreSQL database: {e}")
            return None

    def get_stats(self):
        """Get statistics about users and assignments."""
        connection = self.connect_to_db()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Count total users
                    cursor.execute('SELECT COUNT(*) FROM "secret-santa".users')
                    total_users = cursor.fetchone()[0]
                    
                    # Count assigned friends
                    cursor.execute('SELECT COUNT(*) FROM "secret-santa".secret_friends')
                    total_assignments = cursor.fetchone()[0]
                    
                    # Check if wishes are locked
                    cursor.execute('SELECT wishes_locked FROM "secret-santa".users LIMIT 1')
                    result = cursor.fetchone()
                    wishes_locked = result[0] if result else False
                    
                    return {
                        'total_users': total_users,
                        'total_assignments': total_assignments,
                        'wishes_locked': wishes_locked
                    }
            except (Exception, Error) as e:
                st.error(f"Error fetching stats: {e}")
                return None
            finally:
                connection.close()
        return None

    def assign_friends(self):
        """Run the assign_friends.py script."""
        try:
            result = subprocess.run(
                ['python3', 'utils/assign_friends.py'],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(__file__))
            )
            if result.returncode == 0:
                st.success("✅ Amigos secretos asignados exitosamente!")
                return True
            else:
                st.error(f"❌ Error al asignar amigos: {result.stderr}")
                return False
        except Exception as e:
            st.error(f"❌ Error ejecutando script: {e}")
            return False

    def toggle_wishes_lock(self, lock: bool):
        """Lock or unlock wishes editing for all users."""
        connection = self.connect_to_db()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'UPDATE "secret-santa".users SET wishes_locked = %s',
                        (lock,)
                    )
                    connection.commit()
                    status = "bloqueados" if lock else "desbloqueados"
                    st.success(f"✅ Deseos {status} exitosamente!")
                    return True
            except (Exception, Error) as e:
                st.error(f"Error updating wishes lock: {e}")
                return False
            finally:
                connection.close()
        return False

    def render_dashboard(self):
        """Render the admin dashboard."""
        st.markdown("<h1 style='text-align: center; color: white;'>🔐 Panel de Administrador</h1>",
                    unsafe_allow_html=True)

        # Get statistics
        stats = self.get_stats()
        
        if stats:
            # Display stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("👥 Usuarios Registrados", stats['total_users'])
            with col2:
                st.metric("🎁 Asignaciones", stats['total_assignments'])
            with col3:
                lock_status = "🔒 Bloqueados" if stats['wishes_locked'] else "🔓 Desbloqueados"
                st.metric("Deseos", lock_status)

            st.markdown("---")

            # Admin actions
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎲 Asignar Amigos Secretos")
                st.write("Ejecuta el sorteo y asigna un amigo secreto a cada participante.")
                
                if st.button("🎲 Ejecutar Sorteo", use_container_width=True, type="primary"):
                    with st.spinner("Asignando amigos secretos..."):
                        self.assign_friends()
                        st.rerun()

            with col2:
                st.subheader("🔒 Control de Deseos")
                st.write("Bloquea o desbloquea la edición de deseos de los usuarios.")
                
                if stats['wishes_locked']:
                    if st.button("🔓 Desbloquear Deseos", use_container_width=True):
                        self.toggle_wishes_lock(False)
                        st.rerun()
                else:
                    if st.button("🔒 Bloquear Deseos", use_container_width=True):
                        self.toggle_wishes_lock(True)
                        st.rerun()

        st.markdown("---")
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.is_admin = False
            st.session_state.username = None
            st.session_state.page = "start"
            st.rerun()

    def run(self):
        """Run the admin dashboard."""
        # Check if user is admin
        if 'is_admin' not in st.session_state or not st.session_state.is_admin:
            st.error("⛔ Acceso denegado. Solo administradores.")
            if st.button("Volver"):
                st.session_state.page = "start"
                st.rerun()
        else:
            self.render_dashboard()


def main():
    app = AdminPage()
    app.run()


if __name__ == "__main__":
    main()
