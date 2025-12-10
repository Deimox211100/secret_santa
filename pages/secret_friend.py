import streamlit as st
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.supabase_client import get_supabase_client

# Load environment variables
load_dotenv()


class FriendPage:
    def __init__(self):
        # Get Supabase client
        self.supabase = get_supabase_client()

        # Estilos CSS personalizados
        st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
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

    def fetch_friend_info(self, user_id):
        """Fetch secret friend information for a given user ID."""
        try:
            # First, get the user's ID
            user_response = self.supabase.table('users').select('id').eq('character_name', user_id).execute()
            
            if not user_response.data or len(user_response.data) == 0:
                return None
            
            current_user_id = user_response.data[0]['id']
            
            # Get the secret friend assignment
            assignment_response = self.supabase.table('secret_friends').select('id_secret_friend').eq('user_id', current_user_id).execute()
            
            if not assignment_response.data or len(assignment_response.data) == 0:
                return None
            
            friend_id = assignment_response.data[0]['id_secret_friend']
            
            # Get the friend's information
            friend_response = self.supabase.table('users').select(
                'character_name, character_photo_url, deseo1, link_deseo1, imagen_deseo1, '
                'deseo2, link_deseo2, imagen_deseo2, deseo3, link_deseo3, imagen_deseo3, comentarios_generales'
            ).eq('id', friend_id).execute()
            
            if not friend_response.data or len(friend_response.data) == 0:
                return None
            
            friend = friend_response.data[0]
            
            return {
                "friend_character_name": friend['character_name'],
                "friend_photo_url": friend['character_photo_url'] if friend['character_photo_url'] else "",
                "friend_deseo1": friend['deseo1'] if friend['deseo1'] else "SIN DESEO",
                "friend_link_deseo1": friend['link_deseo1'] if friend['link_deseo1'] else "",
                "friend_imagen_deseo1": friend['imagen_deseo1'] if friend['imagen_deseo1'] else "",
                "friend_deseo2": friend['deseo2'] if friend['deseo2'] else "SIN DESEO",
                "friend_link_deseo2": friend['link_deseo2'] if friend['link_deseo2'] else "",
                "friend_imagen_deseo2": friend['imagen_deseo2'] if friend['imagen_deseo2'] else "",
                "friend_deseo3": friend['deseo3'] if friend['deseo3'] else "SIN DESEO",
                "friend_link_deseo3": friend['link_deseo3'] if friend['link_deseo3'] else "",
                "friend_imagen_deseo3": friend['imagen_deseo3'] if friend['imagen_deseo3'] else "",
                "friend_comentarios_generales": friend.get('comentarios_generales', '')
            }
        except Exception as e:
            st.error(f"Error fetching friend information: {e}")
            return None

    def render_friend_page(self):
        """Render the secret friend page."""
        st.markdown("<h1 style='text-align: center; color: white;'>🎅🏻 Tu Amigo Secreto</h1>",
                    unsafe_allow_html=True)

        username = st.session_state.username
        if st.button("Consultar Amigo Secreto", use_container_width=True):
            friend_info = self.fetch_friend_info(username)
            if friend_info:
                # Character photo and name
                col_profile1, col_profile2 = st.columns([1, 2])
                with col_profile1:
                    if friend_info['friend_photo_url']:
                        st.image(friend_info['friend_photo_url'], use_container_width=True, caption=friend_info['friend_character_name'])
                    else:
                        st.info("Sin foto de perfil")
                
                with col_profile2:
                    st.header(f"Tu amigo secreto es: {friend_info['friend_character_name']} 🎅")
                    st.info("¡Recuerda revisar sus deseos cuidadosamente!")

                st.markdown("---")
                
                # Wishes Section
                st.subheader("🎁 Lista de Deseos")

                # Helper to display a wish
                def display_wish(number, title, wish, link, image, color_emoji):
                   with st.container():
                       st.markdown(f"### {color_emoji} {title}")
                       st.write(wish)
                       
                       if link:
                           st.link_button(f"Ver Referencia del Deseo #{number} 🔗", link)
                       
                       if image:
                           st.image(image, caption=f"Imagen Referencia #{number}", width=300)
                       st.markdown("---")

                # Wish 1
                display_wish(1, "Primera Opción (Favorito 😍)", friend_info['friend_deseo1'], 
                             friend_info['friend_link_deseo1'], friend_info['friend_imagen_deseo1'], "🥇")

                # Wish 2
                display_wish(2, "Segunda Opción (Me encanta)", friend_info['friend_deseo2'],
                             friend_info['friend_link_deseo2'], friend_info['friend_imagen_deseo2'], "🥈")

                # Wish 3
                if friend_info['friend_deseo3'] != "SIN DESEO":
                     display_wish(3, "Tercera Opción (Si te sientes generoso 😇)", friend_info['friend_deseo3'],
                             friend_info['friend_link_deseo3'], friend_info['friend_imagen_deseo3'], "🥉")

                # General Comments
                if friend_info['friend_comentarios_generales']:
                    st.markdown("### 📝 Notas Importantes")
                    st.warning(friend_info['friend_comentarios_generales'])
            
            else:
                st.warning("Aún no se ha hecho el sorteo, Calma Tigre!.")

        if st.button("Volver", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    def run(self):
        """Run the Streamlit application."""
        if 'username' in st.session_state:
            self.render_friend_page()
        else:
            st.error("Por favor inicia sesión.")


def main():
    app = FriendPage()
    app.run()


if __name__ == "__main__":
    main()