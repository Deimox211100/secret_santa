import streamlit as st
import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class LoginPage:
    def __init__(self):
        # Configuración de la base de datos desde las variables de entorno
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'dbname': os.getenv('DB_NAME'),
            'port': os.getenv('DB_PORT', '5432')
        }

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

    def connect_to_db(self):
        """Conectar a la base de datos PostgreSQL."""
        try:
            connection = psycopg2.connect(**self.db_config)
            return connection
        except (Exception, Error) as e:
            st.error(f"Error al conectar con la base de datos PostgreSQL: {e}")
            return None

    def check_credentials(self, username, password):
        """Verificar las credenciales del usuario en la base de datos."""
        connection = self.connect_to_db()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Verificar si el usuario existe y la contraseña es correcta
                    cursor.execute("""
                    SELECT * FROM "secret-santa".users WHERE estacion = %s AND password = %s
                    """, (username, password))
                    user = cursor.fetchone()
                    return user is not None
            except (Exception, Error) as e:
                st.error(f"Error al verificar las credenciales: {e}")
                return False
            finally:
                if connection:
                    connection.close()
        return False

    def render_login_page(self):
        """Renderizar la página de login."""
        st.markdown("<h1 style='text-align: center; color: white;'>🎅🏻 Iniciar Sesión - Amigo Secreto</h1>",
                    unsafe_allow_html=True)

        # Columnas para centrar la imagen
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.image(
                "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3lkZmJkZGtuMmkwam1jbDh2aWpsaGl2NHBybjA5MHQ3MG96M214dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9JrvLb0fnrn7k1ZjhX/giphy.gif",
                use_container_width =True
            )
        with col3:
            st.write(' ')

        # Columnas para centrar el formulario
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Campos de formulario de login
            username = st.text_input("Nombre de Usuario")
            password = st.text_input("Contraseña", type="password")

            if st.button("Iniciar Sesión", use_container_width=True):
                if username and password:
                    # Verificar las credenciales
                    if self.check_credentials(username, password):
                        # Establecer estado de sesión
                        st.session_state.logged_in = True
                        st.session_state.username = username

                        # Cambiar a la página de inicio
                        st.session_state.page = "home"
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas.")
                else:
                    st.error("Por favor ingresa tu nombre de usuario y contraseña.")

            # Botón para volver al inicio
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