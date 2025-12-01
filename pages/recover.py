import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.supabase_client import get_supabase_client

# Load environment variables
load_dotenv()

class RecoverPage:
    def __init__(self):
        # Get Supabase client
        self.supabase = get_supabase_client()

        # Custom CSS
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

    def get_character_by_email(self, email):
        """Fetch character name and photo by email."""
        try:
            response = self.supabase.table('users').select('character_name, character_photo_url').eq('email', email).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            st.error(f"Error al buscar el personaje: {e}")
            return None

    def render_recover_page(self):
        """Render the recovery page."""
        st.markdown("<h1 style='text-align: center; color: white;'>🔍 Recuperar Personaje</h1>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <p style='text-align: center; color: #ccc;'>
                Ingresa el correo electrónico con el que te registraste para ver tu personaje.
            </p>
            """, unsafe_allow_html=True)

            email = st.text_input("Correo Electrónico")

            if st.button("Buscar Personaje", use_container_width=True):
                if email:
                    user_data = self.get_character_by_email(email)
                    if user_data:
                        character_name = user_data['character_name']
                        photo_url = user_data.get('character_photo_url')

                        st.success("¡Personaje encontrado!")
                        
                        st.markdown(f"<h2 style='text-align: center; color: #FF9800;'>Tu personaje es: {character_name}</h2>", unsafe_allow_html=True)
                        
                        if photo_url:
                            sub_col1, sub_col2, sub_col3 = st.columns([1, 2, 1])
                            with sub_col2:
                                st.image(photo_url, use_container_width=True, caption=character_name)
                    else:
                        st.error("No se encontró ningún personaje asociado a este correo.")
                else:
                    st.warning("Por favor ingresa un correo electrónico.")

            st.markdown("---")
            if st.button("Volver al Inicio", use_container_width=True):
                st.session_state.page = "start"
                st.rerun()

    def run(self):
        self.render_recover_page()

def main():
    app = RecoverPage()
    app.run()

if __name__ == "__main__":
    main()
