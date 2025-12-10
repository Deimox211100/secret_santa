import streamlit as st
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.supabase_client import get_supabase_client

# Cargar variables de entorno
load_dotenv()


class LoginPage:
    def __init__(self):
        # Get Supabase client
        self.supabase = get_supabase_client()

        # Estilos CSS personalizados
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

    def check_credentials(self, username, password):
        """Verificar las credenciales del usuario en la base de datos."""
        try:
            # Check if admin
            admin_response = self.supabase.table('admin').select('*').eq('username', username).eq('password', password).execute()
            
            if admin_response.data and len(admin_response.data) > 0:
                return {'is_admin': True, 'username': username}
            
            # Check if regular user
            user_response = self.supabase.table('users').select('*').ilike('character_name', username).eq('password', password).execute()
            
            if user_response.data and len(user_response.data) > 0:
                user = user_response.data[0]
                return {
                    'is_admin': False, 
                    'username': user['character_name'],
                    'character_photo_url': user.get('character_photo_url')
                }
            
            return None
        except Exception as e:
            st.error(f"Error al verificar las credenciales: {e}")
            return None

    def render_login_page(self):
        """Renderizar la página de login."""
        # Título centrado y estilizado
        st.markdown("<h1 style='text-align: center; color: white; font-size: 2.5em;'>🎄 Iniciar Sesión 🎄</h1>",
                    unsafe_allow_html=True)

        # Columnas para centrar la imagen
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.image(
                "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjRvdDRjejl5bXloZTR4MW05NG1hNnphOGlzemd2YnBndXJob2hiMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9JrvLb0fnrn7k1ZjhX/giphy.gif",
                use_container_width=True
            )
        with col3:
            st.write(' ')

        # Contenedor para centrar los formularios y botones
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Campos de entrada
            username = st.text_input("Personaje", max_chars=100)
            password = st.text_input("Contraseña", type="password")

            # Botón de login
            if st.button("Iniciar Sesión", use_container_width=True):
                if username and password:
                    # Clean input
                    username = username.strip().lower()
                    # Verificar las credenciales
                    result = self.check_credentials(username, password)
                    if result:
                        # Establecer estado de sesión
                        st.session_state.logged_in = True
                        st.session_state.username = result['username']
                        st.session_state.is_admin = result['is_admin']
                        st.session_state.character_photo_url = result.get('character_photo_url')

                        # Cambiar a la página correspondiente
                        if result['is_admin']:
                            st.session_state.page = "admin"
                        else:
                            st.session_state.page = "home"
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas.")
                else:
                    st.error("Por favor ingresa tu personaje y contraseña.")

            # Botón de volver
            if st.button("Volver", use_container_width=True):
                st.session_state.page = "start"
                st.rerun()

    def run(self):
        """Ejecutar la página de login."""
        self.render_login_page()


def main():
    login_page = LoginPage()
    login_page.run()


if __name__ == "__main__":
    main()