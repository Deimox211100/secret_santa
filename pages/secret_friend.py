import streamlit as st
import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FriendPage:
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

    def connect_to_db(self):
        """Establish a database connection."""
        try:
            connection = psycopg2.connect(**self.db_config)
            return connection
        except (Exception, Error) as e:
            st.error(f"Error connecting to the PostgreSQL database: {e}")
            return None

    def fetch_friend_info(self, user_id):
        """Fetch secret friend information for a given user ID."""
        query = """
        SELECT 
            character_name,
            character_photo_url,
            deseo1,
            link_deseo1,
            imagen_deseo1,
            deseo2,
            link_deseo2,
            imagen_deseo2,
            deseo3,
            link_deseo3,
            imagen_deseo3
        FROM "secret-santa".secret_friends sf
        JOIN "secret-santa".users u
        ON sf.id_secret_friend = u.id
        WHERE sf.user_id = (SELECT id FROM "secret-santa".users WHERE character_name = %s);
        """
        connection = self.connect_to_db()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    result = cursor.fetchone()
                    return {
                        "friend_character_name": result[0],
                        "friend_photo_url": result[1] if result[1] else "",
                        "friend_deseo1": result[2] if result[2] else "SIN DESEO",
                        "friend_link_deseo1": result[3] if result[3] else "",
                        "friend_imagen_deseo1": result[4] if result[4] else "",
                        "friend_deseo2": result[5] if result[5] else "SIN DESEO",
                        "friend_link_deseo2": result[6] if result[6] else "",
                        "friend_imagen_deseo2": result[7] if result[7] else "",
                        "friend_deseo3": result[8] if result[8] else "SIN DESEO",
                        "friend_link_deseo3": result[9] if result[9] else "",
                        "friend_imagen_deseo3": result[10] if result[10] else ""
                    } if result else None
            except (Exception, Error) as e:
                st.error(f"Error fetching friend information: {e}")
            finally:
                connection.close()
        return None

    def render_form(self):
        """Render the form and display friend information."""
        st.markdown("<h1 style='text-align: center; color: white;'>🎅🏻 Información de Tu Amigo Secreto 🎅🏻</h1>",
                    unsafe_allow_html=True)

        username = st.session_state.username
        if st.button("Consultar Amigo Secreto", use_container_width=True):
            friend_info = self.fetch_friend_info(username)
            if friend_info:
                st.success(f"🎅🏻 Tu amigo secreto es: **{friend_info['friend_character_name']}**")
                
                # Display character photo if available
                if friend_info['friend_photo_url']:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.image(friend_info['friend_photo_url'], width=200, caption=friend_info['friend_character_name'])
                
                # Display wishes with images
                st.markdown("---")
                st.markdown("### 🎁 Deseos")
                
                # Wish 1
                st.markdown(f"**Deseo #1:** {friend_info['friend_deseo1']}")
                if friend_info['friend_link_deseo1']:
                    st.markdown(f"[🔗 Ver enlace]({friend_info['friend_link_deseo1']})")
                if friend_info['friend_imagen_deseo1']:
                    st.image(friend_info['friend_imagen_deseo1'], width=300, caption="Imagen Deseo #1")
                
                # Wish 2
                st.markdown(f"**Deseo #2:** {friend_info['friend_deseo2']}")
                if friend_info['friend_link_deseo2']:
                    st.markdown(f"[🔗 Ver enlace]({friend_info['friend_link_deseo2']})")
                if friend_info['friend_imagen_deseo2']:
                    st.image(friend_info['friend_imagen_deseo2'], width=300, caption="Imagen Deseo #2")
                
                # Wish 3
                if friend_info['friend_deseo3'] != "SIN DESEO":
                    st.markdown(f"**Deseo #3:** {friend_info['friend_deseo3']}")
                    if friend_info['friend_link_deseo3']:
                        st.markdown(f"[🔗 Ver enlace]({friend_info['friend_link_deseo3']})")
                    if friend_info['friend_imagen_deseo3']:
                        st.image(friend_info['friend_imagen_deseo3'], width=300, caption="Imagen Deseo #3")
            else:
                st.warning("Aún no se ha echo el sorteo, Calma Tigre!.")

        if st.button("Volver", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    def run(self):
        """Run the Streamlit application."""
        self.render_form()


def main():
    app = FriendPage()
    app.run()


if __name__ == "__main__":
    main()