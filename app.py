import streamlit as st
import json
import psycopg2
from psycopg2 import Error
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SecretSantaApp:
    def __init__(self):
        # Database connection configuration from environment variables
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'dbname': os.getenv('DB_NAME'),
            'port': os.getenv('DB_PORT', '5432')
        }

        # Initialize session state for form data
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize session state variables to persist form data."""
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {
                'nombre': '',
                'apellido': '',
                'deseo1': '',
                'link_deseo1': '',
                'deseo2': '',
                'link_deseo2': '',
                'deseo3': '',
                'link_deseo3': '',
                'estacion': None
            }

    def connect_to_db(self):
        """Establish a database connection."""
        try:
            connection = psycopg2.connect(**self.db_config)
            return connection
        except (Exception, Error) as e:
            st.error(f"Error connecting to the PostgreSQL database: {e}")
            return None

    def load_stations(self):
        """Load available stations from JSON file."""
        try:
            with open("utils/stations.json", "r", encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error("Stations file not found.")
            return []
        except json.JSONDecodeError:
            st.error("Error decoding stations JSON file.")
            return []

    def get_selected_stations(self):
        """Retrieve already selected stations from the database."""
        connection = self.connect_to_db()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT estacion FROM "secret-santa".users')
                    selected_stations = [row[0] for row in cursor.fetchall()]
                return selected_stations
            except (Exception, Error) as e:
                st.error(f"Error retrieving selected stations: {e}")
                return []
            finally:
                if connection:
                    connection.close()
        return []

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
        if not data['apellido']:
            errors.append("El apellido es obligatorio.")
        if not data['deseo1']:
            errors.append("El Deseo #1 es obligatorio.")
        if not data['deseo2']:
            errors.append("El Deseo #2 es obligatorio.")
        if not data['estacion']:
            errors.append("Debes seleccionar una estación.")

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
                    (nombre, apellido, deseo1, link_deseo1, deseo2, link_deseo2, 
                     deseo3, link_deseo3, estacion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        st.title("Registro de Intercambio de Deseos")

        # Load stations
        all_stations = self.load_stations()
        selected_stations = self.get_selected_stations()
        available_stations = [station for station in all_stations
                              if station not in selected_stations]

        # Prepare form data from session state
        form_data = st.session_state.form_data

        with st.form("registro_form", clear_on_submit=False):
            # Input fields with session state preservation
            nombre = st.text_input("Nombre",
                                   max_chars=100,
                                   value=form_data['nombre'])
            apellido = st.text_input("Apellido",
                                     max_chars=100,
                                     value=form_data['apellido'])
            deseo1 = st.text_input("Deseo #1",
                                   value=form_data['deseo1'])
            link_deseo1 = st.text_input("Link Deseo #1",
                                        value=form_data['link_deseo1'])
            deseo2 = st.text_input("Deseo #2",
                                   value=form_data['deseo2'])
            link_deseo2 = st.text_input("Link Deseo #2",
                                        value=form_data['link_deseo2'])
            deseo3 = st.text_input("Deseo #3 (Opcional)",
                                   value=form_data['deseo3'])
            link_deseo3 = st.text_input("Link Deseo #3 (Opcional)",
                                        value=form_data['link_deseo3'])

            # Station selection with preserved state
            estacion = st.selectbox(
                "Elige tu estación",
                available_stations,
                index=available_stations.index(form_data['estacion'])
                if form_data['estacion'] in available_stations
                else 0
            )

            # Form submission
            submitted = st.form_submit_button("Registrar")

            if submitted:
                # Update session state with current form values
                st.session_state.form_data = {
                    'nombre': nombre,
                    'apellido': apellido,
                    'deseo1': deseo1,
                    'link_deseo1': link_deseo1,
                    'deseo2': deseo2,
                    'link_deseo2': link_deseo2,
                    'deseo3': deseo3,
                    'link_deseo3': link_deseo3,
                    'estacion': estacion
                }

                # Prepare data for validation and saving
                data = st.session_state.form_data

                # Validate inputs
                validation_result = self.validate_inputs(data)
                if validation_result is True:
                    # Attempt to save to database
                    if self.save_to_db(tuple(data.values())):
                        # Reset session state after successful submission
                        st.session_state.form_data = {
                            'nombre': '',
                            'apellido': '',
                            'deseo1': '',
                            'link_deseo1': '',
                            'deseo2': '',
                            'link_deseo2': '',
                            'deseo3': '',
                            'link_deseo3': '',
                            'estacion': None
                        }
                        st.rerun()
                else:
                    # If validation fails, error message is already shown
                    # Data remains in the form due to session state
                    pass

    def run(self):
        """Run the Streamlit application."""
        self.render_form()


def main():
    app = SecretSantaApp()
    app.run()


if __name__ == "__main__":
    main()