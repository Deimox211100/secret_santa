import streamlit as st
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.supabase_client import get_supabase_client

# Load environment variables
load_dotenv()


class ProfilePage:
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

    def get_user_info(self, username):
        """Fetch user information from the database."""
        try:
            response = self.supabase.table('users').select(
                'character_name, character_photo_url, deseo1, link_deseo1, deseo2, link_deseo2, deseo3, link_deseo3, comentarios_generales, wishes_locked'
            ).eq('character_name', username).execute()
            
            if response.data and len(response.data) > 0:
                user = response.data[0]
                return (
                    user['character_name'],
                    user.get('character_photo_url'),
                    user['deseo1'],
                    user['link_deseo1'],
                    user['deseo2'],
                    user['link_deseo2'],
                    user['deseo3'],
                    user['link_deseo3'],
                    user.get('comentarios_generales', ''),
                    user['wishes_locked']
                )
            return None
        except Exception as e:
            st.error(f"Error fetching user info: {e}")
            return None

    def update_user_info(self, username, deseo1, link_deseo1, deseo2, link_deseo2, deseo3, link_deseo3, comentarios_generales):
        """Update user information in the database."""
        try:
            response = self.supabase.table('users').update({
                'deseo1': deseo1,
                'link_deseo1': link_deseo1,
                'deseo2': deseo2,
                'link_deseo2': link_deseo2,
                'deseo3': deseo3,
                'link_deseo3': link_deseo3,
                'comentarios_generales': comentarios_generales
            }).eq('character_name', username).execute()
            
            if response.data:
                st.success("Información actualizada exitosamente.")
                return True
            return False
        except Exception as e:
            st.error(f"Error updating user info: {e}")
            return False

    def render_form(self):
        """Render the profile form."""
        st.markdown("<h1 style='text-align: center; color: white;'>🎁 Mi Perfil</h1>", unsafe_allow_html=True)

        username = st.session_state.username
        user_info = self.get_user_info(username)

        if user_info:
            character_name, character_photo_url, deseo1, link_deseo1, deseo2, link_deseo2, deseo3, link_deseo3, comentarios_generales, wishes_locked = user_info

            # Display character photo
            if character_photo_url:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(character_photo_url, width=200, caption=character_name)

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

            st.markdown("### 📝 Comentarios Generales")
            comentarios_generales_edit = st.text_area("Comentarios sobre tus deseos, tallas, colores preferidos, etc.", value=comentarios_generales, disabled=wishes_locked)

            # Save button (only if wishes not locked)
            if not wishes_locked:
                if st.button("Guardar Cambios", use_container_width=True):
                    self.update_user_info(username, deseo1_edit, link_deseo1_edit, deseo2_edit, link_deseo2_edit,
                                          deseo3_edit, link_deseo3_edit, comentarios_generales_edit)

            if st.button("Volver", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()
        else:
            st.error("No se pudo cargar la información del usuario.")

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