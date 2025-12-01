import streamlit as st
import json
import psycopg2
from psycopg2 import Error
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class RegisterPage:
    def __init__(self):
        # Database connection configuration from environment variables
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

        # Initialize session state for form data
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize session state variables to persist form data."""
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {
                'nombre': '',
                'email': '',
                'deseo1': '',
                'link_deseo1': '',
                'imagen_deseo1': '',
                'deseo2': '',
                'link_deseo2': '',
                'imagen_deseo2': '',
                'deseo3': '',
                'link_deseo3': '',
                'imagen_deseo3': '',
                'username': None,
                'password': ''
            }

    def connect_to_db(self):
        """Establish a database connection."""
        try:
            connection = psycopg2.connect(**self.db_config)
            return connection
        except (Exception, Error) as e:
            st.error(f"Error connecting to the PostgreSQL database: {e}")
            return None

    def load_characters(self):
        """Load available characters from the configured characters file."""
        try:
            from utils.config_loader import load_characters
            characters_data = load_characters()
            return characters_data
        except FileNotFoundError as e:
            st.error(f"Characters file not found: {e}")
            return []
        except Exception as e:
            st.error(f"Error loading characters: {e}")
            return []

    def get_selected_characters(self):
        """Retrieve already selected characters from the database."""
        connection = self.connect_to_db()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT character_name FROM "secret-santa".users')
                    selected_characters = [row[0] for row in cursor.fetchall()]
                return selected_characters
            except (Exception, Error) as e:
                st.error(f"Error retrieving selected characters: {e}")
                return []
            finally:
                if connection:
                    connection.close()
        return []

    def is_valid_email(self, email):
        """Validate email format."""
        if not email:
            return False
        
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        return email_pattern.match(email) is not None

    def is_valid_url(self, url):
        """Validate URL format."""
        if not url:  # Allow empty URLs
            return True

        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None

    def validate_inputs(self, data):
        """Validate user inputs with more robust checks."""
        # Basic validation with specific error messages
        errors = []

        if not data['nombre']:
            errors.append("El nombre es obligatorio.")
        if not data['email']:
            errors.append("El correo electrónico es obligatorio.")
        elif not self.is_valid_email(data['email']):
            errors.append("El correo electrónico no es válido.")
        if not data['deseo1']:
            errors.append("El Deseo #1 es obligatorio.")
        if not data['deseo2']:
            errors.append("El Deseo #2 es obligatorio.")
        if not data['username']:
            errors.append("Debes seleccionar un personaje.")
        if not data['password']:  # Check if password is provided
            errors.append("La contraseña es obligatoria.")

        # URL validations
        if data['link_deseo1'] and not self.is_valid_url(data['link_deseo1']):
            errors.append("El enlace del Deseo #1 no es válido.")

        if data['link_deseo2'] and not self.is_valid_url(data['link_deseo2']):
            errors.append("El enlace del Deseo #2 no es válido.")

        # If there are errors, display them and return False
        if errors:
            for error in errors:
                st.error(error)
            return False

        return True

    def save_to_db(self, data):
        """Save user data to the database."""
        connection = self.connect_to_db()
        if connection:
            try:
                with connection.cursor() as cursor:
                    insert_query = """
                    INSERT INTO "secret-santa".users 
                    (nombre, email, deseo1, link_deseo1, imagen_deseo1, deseo2, link_deseo2, imagen_deseo2,
                     deseo3, link_deseo3, imagen_deseo3, character_name, character_photo_url, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, data)
                    connection.commit()
                    st.success("Registro guardado exitosamente.")
                    return True
            except (Exception, Error) as e:
                st.error(f"Error al guardar el registro: {e}")
                return False
            finally:
                if connection:
                    connection.close()
        return False

    def render_form(self):
        """Render the main registration form."""
        st.markdown("<h1 style='text-align: center; color: white;'>🎅🏻 Registrate para participar 🎅🏻</h1>",
                    unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.image(
                "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2Vnb2dmcDBkMnNpNHN5cG9vYm55NDY2MG8wdzRwNjlsbDU3ZWk4eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VKwspRV2pafJu/giphy.gif",
                use_container_width =True
            )
        with col3:
            st.write(' ')

        # Contenedor para centrar los formularios y botones
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Load characters
            all_characters = self.load_characters()
            selected_characters = self.get_selected_characters()
            selected_character_names = [char['name'] for char in selected_characters] if selected_characters and isinstance(selected_characters[0], dict) else selected_characters
            available_characters = [char for char in all_characters
                                   if char['name'] not in selected_character_names]

            # Prepare form data from session state
            form_data = st.session_state.form_data

            with st.form("registro_form", clear_on_submit=False):
                # Input fields with session state preservation
                nombre = st.text_input("Nombre",
                                       max_chars=100,
                                       value=form_data['nombre'])
                email = st.text_input("Correo Electrónico",
                                         max_chars=255,
                                         value=form_data['email'],
                                         placeholder="ejemplo@correo.com")
                
                st.markdown("### 🎁 Deseo #1")
                deseo1 = st.text_input("Deseo #1",
                                       value=form_data['deseo1'],
                                       label_visibility="collapsed")
                link_deseo1 = st.text_input("Link Deseo #1 (Opcional)",
                                            value=form_data['link_deseo1'])
                imagen_deseo1 = st.text_input("URL de Imagen Deseo #1 (Opcional)",
                                             value=form_data['imagen_deseo1'],
                                             placeholder="https://ejemplo.com/imagen.jpg")
                
                st.markdown("### 🎁 Deseo #2")
                deseo2 = st.text_input("Deseo #2",
                                       value=form_data['deseo2'],
                                       label_visibility="collapsed")
                link_deseo2 = st.text_input("Link Deseo #2 (Opcional)",
                                            value=form_data['link_deseo2'])
                imagen_deseo2 = st.text_input("URL de Imagen Deseo #2 (Opcional)",
                                             value=form_data['imagen_deseo2'],
                                             placeholder="https://ejemplo.com/imagen.jpg")
                
                st.markdown("### 🎁 Deseo #3 (Opcional)")
                deseo3 = st.text_input("Deseo #3 (Opcional)",
                                       value=form_data['deseo3'],
                                       label_visibility="collapsed")
                link_deseo3 = st.text_input("Link Deseo #3 (Opcional)",
                                            value=form_data['link_deseo3'])
                imagen_deseo3 = st.text_input("URL de Imagen Deseo #3 (Opcional)",
                                             value=form_data['imagen_deseo3'],
                                             placeholder="https://ejemplo.com/imagen.jpg")

                # Character selection with preserved state
                character_names = [char['name'] for char in available_characters]
                selected_character_name = st.selectbox(
                    "Elige tu personaje",
                    character_names,
                    index=character_names.index(form_data['username'])
                    if form_data['username'] in character_names
                    else 0
                )
                
                # Get the selected character data
                selected_character = next((char for char in available_characters if char['name'] == selected_character_name), None)
                username = selected_character['name'] if selected_character else selected_character_name
                character_photo_url = selected_character['photo_url'] if selected_character else ""

                # Password field
                password = st.text_input("Contraseña", type="password", value=form_data['password'])

                # Form submission buttons
                col_back, col_submit = st.columns(2)

                with col_back:
                    if st.form_submit_button("Volver", use_container_width=True):
                        st.session_state.page = "start"
                        st.rerun()

                with col_submit:
                    submitted = st.form_submit_button("Registrar", use_container_width=True)

                if submitted:
                    # Update session state with current form values
                    st.session_state.form_data = {
                        'nombre': nombre,
                        'email': email,
                        'deseo1': deseo1,
                        'link_deseo1': link_deseo1,
                        'imagen_deseo1': imagen_deseo1,
                        'deseo2': deseo2,
                        'link_deseo2': link_deseo2,
                        'imagen_deseo2': imagen_deseo2,
                        'deseo3': deseo3,
                        'link_deseo3': link_deseo3,
                        'imagen_deseo3': imagen_deseo3,
                        'username': username,
                        'password': password
                    }

                    # Validate inputs
                    validation_result = self.validate_inputs(st.session_state.form_data)
                    if validation_result is True:
                        # Prepare data tuple with character photo URL and images
                        data_to_save = (nombre, email, deseo1, link_deseo1, imagen_deseo1,
                                       deseo2, link_deseo2, imagen_deseo2,
                                       deseo3, link_deseo3, imagen_deseo3,
                                       username, character_photo_url, password)
                        # Attempt to save to database
                        if self.save_to_db(data_to_save):
                            # Cambiar a la página de login
                            st.session_state.form_data = {}  # Clear form data
                            st.session_state.page = "login"
                            st.rerun()

    def run(self):
        """Run the Streamlit application."""
        self.render_form()


def main():
    app = RegisterPage()
    app.run()


if __name__ == "__main__":
    main()