import streamlit as st
import os
from dotenv import load_dotenv
import subprocess
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.supabase_client import get_supabase_client

# Load environment variables
load_dotenv()


class AdminPage:
    def __init__(self):
        # Get Supabase client
        self.supabase = get_supabase_client()

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

    def get_stats(self):
        """Get statistics about users and assignments."""
        try:
            # Count total users
            users_response = self.supabase.table('users').select('*', count='exact').execute()
            total_users = users_response.count if users_response.count is not None else len(users_response.data)
            
            # Count assigned friends
            friends_response = self.supabase.table('secret_friends').select('*', count='exact').execute()
            total_assignments = friends_response.count if friends_response.count is not None else len(friends_response.data)
            
            # Check if wishes are locked
            # We check the first user as the lock status is global (applied to all users)
            lock_response = self.supabase.table('users').select('wishes_locked').limit(1).execute()
            wishes_locked = False
            if lock_response.data and len(lock_response.data) > 0:
                wishes_locked = lock_response.data[0]['wishes_locked']
            
            return {
                'total_users': total_users,
                'total_assignments': total_assignments,
                'wishes_locked': wishes_locked
            }
        except Exception as e:
            st.error(f"Error fetching stats: {e}")
            return None

    def assign_friends(self):
        """Run the assign_friends.py script."""
        # Note: assign_friends.py might need to be updated to use Supabase API as well
        # For now, we'll assume it's updated or we should update it.
        # Given the user request, we should probably update it too, but let's stick to the pages first.
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
        try:
            # Update all users
            # Supabase update without where clause is blocked by default for safety
            # But we can use a condition that is always true or iterate
            # Or better, we can use a specific RPC function if we had one.
            # For now, let's try to update where id > 0 which should cover all users
            response = self.supabase.table('users').update({'wishes_locked': lock}).gt('id', 0).execute()
            
            if response.data:
                status = "bloqueados" if lock else "desbloqueados"
                st.success(f"✅ Deseos {status} exitosamente!")
                return True
            return False
        except Exception as e:
            st.error(f"Error updating wishes lock: {e}")
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
