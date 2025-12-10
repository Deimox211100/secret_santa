import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.supabase_client import get_supabase_client

# Load environment variables
load_dotenv()

class ChangePasswordPage:
    def __init__(self):
        # Get Supabase client
        self.supabase = get_supabase_client()

        # Custom CSS (consistent with other pages)
        st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
        }
        .stTextInput > div > div > input {
            color: white;
            background-color: #333;
            border: 1px solid #555;
        }
        .stButton > button {
            color: white;
            background-color: #4CAF50;
            border: none;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True)

    def verify_user(self, character_name, email):
        """Verify if character name and email match a user."""
        try:
            response = self.supabase.table('users').select('*').ilike('character_name', character_name).eq('email', email).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]['id']
            return None
        except Exception as e:
            st.error(f"Error al verificar usuario: {e}")
            return None

    def update_password(self, user_id, new_password):
        """Update the user's password."""
        try:
            self.supabase.table('users').update({'password': new_password}).eq('id', user_id).execute()
            return True
        except Exception as e:
            st.error(f"Error al actualizar la contraseña: {e}")
            return False

    def render_page(self):
        """Render the change password page."""
        st.markdown("<h1 style='text-align: center; color: white;'>🔄 Cambiar Contraseña</h1>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <p style='text-align: center; color: #ccc;'>
                Ingresa tu Personaje y Correo Electrónico para verificar tu identidad.
            </p>
            """, unsafe_allow_html=True)

            character_name = st.text_input("Personaje")
            email = st.text_input("Correo Electrónico")
            
            # State management for verification
            if 'verified_user_id' not in st.session_state:
                st.session_state.verified_user_id = None

            if st.session_state.verified_user_id is None:
                if st.button("Verificar Identidad", use_container_width=True):
                    if character_name and email:
                        user_id = self.verify_user(character_name, email)
                        if user_id:
                            st.session_state.verified_user_id = user_id
                            st.success("¡Identidad verificada! Ahora puedes cambiar tu contraseña.")
                            st.rerun()
                        else:
                            st.error("Los datos no coinciden con nuestros registros.")
                    else:
                        st.warning("Por favor completa todos los campos.")
            else:
                # Show password fields after verification
                st.info(f"Cambiando contraseña para: {character_name}")
                new_password = st.text_input("Nueva Contraseña", type="password")
                confirm_password = st.text_input("Confirmar Nueva Contraseña", type="password")

                if st.button("Actualizar Contraseña", use_container_width=True):
                    if new_password and confirm_password:
                        if new_password == confirm_password:
                            if self.update_password(st.session_state.verified_user_id, new_password):
                                st.success("¡Contraseña actualizada exitosamente!")
                                # Clear state
                                st.session_state.verified_user_id = None
                                # Redirect to login
                                if st.button("Ir a Iniciar Sesión", use_container_width=True):
                                    st.session_state.page = "login"
                                    st.rerun()
                            else:
                                st.error("No se pudo actualizar la contraseña. Intenta nuevamente.")
                        else:
                            st.error("Las contraseñas no coinciden.")
                    else:
                        st.warning("Por favor ingresa y confirma la nueva contraseña.")
                
                if st.button("Cancelar", use_container_width=True):
                     st.session_state.verified_user_id = None
                     st.rerun()

            st.markdown("---")
            if st.button("Volver al Inicio", use_container_width=True):
                st.session_state.page = "start"
                st.session_state.verified_user_id = None # Security cleanup
                st.rerun()

    def run(self):
        self.render_page()

def main():
    app = ChangePasswordPage()
    app.run()

if __name__ == "__main__":
    main()
