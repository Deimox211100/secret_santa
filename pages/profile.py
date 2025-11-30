import streamlit as st
import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ProfilePage:
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
        .stTextInput > div > div > input {
            color: white;
            background-color: #333;
            border: 1px solid #555;
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

    def get_user_info(self, username):
        """Fetch user information from the database."""
        connection = self.connect_to_db()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                    SELECT character_name, deseo1, link_deseo1, deseo2, link_deseo2, deseo3, link_deseo3, wishes_locked 
                    FROM "secret-santa".users WHERE character_name = %s
                    """, (username,))
                    return cursor.fetchone()
            except (Exception, Error) as e:
                st.error(f"Error fetching user info: {e}")
                return None
            finally:
                connection.close()
        return None

    def update_user_info(self, username, deseo1, link_deseo1, deseo2, link_deseo2, deseo3, link_deseo3):
        """Update user information in the database."""
        connection = self.connect_to_db()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                    UPDATE "secret-santa".users
                    SET deseo1 = %s, link_deseo1 = %s, deseo2 = %s, link_deseo2 = %s, deseo3 = %s, link_deseo3 = %s
                    WHERE character_name = %s
                    """, (deseo1, link_deseo1, deseo2, link_deseo2, deseo3, link_deseo3, username))
                    connection.commit()
                    st.success("Información actualizada exitosamente.")
            except (Exception, Error) as e:
                st.error(f"Error updating user info: {e}")
            finally:
                connection.close()

    def render_form(self):
        """Render the profile form with editable fields."""
        st.markdown(f"<h1 style='text-align: center; color: white;'>🎅🏻 Perfil - {st.session_state.username} 🎅🏻</h1>",
                    unsafe_allow_html=True)

        username = st.session_state.username
        user_info = self.get_user_info(username)

        if user_info:
            character_name, deseo1, link_deseo1, deseo2, link_deseo2, deseo3, link_deseo3, wishes_locked = user_info

            # Check if wishes are locked
            if wishes_locked:
                st.warning("⚠️ La edición de deseos está bloqueada por el administrador.")

            # Display editable fields
            st.subheader("🎁 Tus Deseos:")
            deseo1_edit = st.text_input("Deseo 1", value=deseo1, disabled=wishes_locked)
            link_deseo1_edit = st.text_input("Link del Deseo 1", value=link_deseo1, disabled=wishes_locked)

            deseo2_edit = st.text_input("Deseo 2", value=deseo2, disabled=wishes_locked)
            link_deseo2_edit = st.text_input("Link del Deseo 2", value=link_deseo2, disabled=wishes_locked)

            deseo3_edit = st.text_input("Deseo 3", value=deseo3, disabled=wishes_locked)
            link_deseo3_edit = st.text_input("Link del Deseo 3", value=link_deseo3, disabled=wishes_locked)

            # Save button (only if wishes not locked)
            if not wishes_locked:
                if st.button("Guardar Cambios", use_container_width=True):
                    self.update_user_info(username, deseo1_edit, link_deseo1_edit, deseo2_edit, link_deseo2_edit,
                                          deseo3_edit, link_deseo3_edit)

            if st.button("Volver", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()


    def run(self):
        """Run the Streamlit application."""
        if 'username' in st.session_state:
            self.render_form()
        else:
            st.error("Por favor inicia sesión.")

def main():
    app = ProfilePage()
    app.run()

if __name__ == "__main__":
    # Simulate user session (replace with actual login logic)
    if 'username' not in st.session_state:
        st.session_state.username = "Homer Simpson"  # Cambia por el username real
    main()