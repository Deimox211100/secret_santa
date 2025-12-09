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
                # Styles for the letter
                st.markdown("""
                <style>
                .letter-container {
                    background-color: #f8f9fa;
                    color: #2c3e50;
                    padding: 40px;
                    border-radius: 10px;
                    font-family: 'Courier New', Courier, monospace;
                    line-height: 1.6;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    margin: 20px 0;
                    border: 2px solid #e0e0e0;
                    background-image: repeating-linear-gradient(0deg, transparent, transparent 29px, #d1d1d1 30px);
                }
                .letter-header {
                    font-size: 1.5em;
                    font-weight: bold;
                    margin-bottom: 20px;
                }
                .letter-body {
                    font-size: 1.2em;
                }
                .letter-wish {
                    margin-left: 20px;
                    margin-bottom: 15px;
                }
                .letter-footer {
                    margin-top: 40px;
                    text-align: right;
                    font-size: 1.3em;
                    font-style: italic;
                }
                .highlight-wish {
                    color: #c0392b;
                    font-weight: bold;
                }
                a {
                    color: #d35400;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                </style>
                """, unsafe_allow_html=True)

                # Character photo
                if friend_info['friend_photo_url']:
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.image(friend_info['friend_photo_url'], width=150, caption=friend_info['friend_character_name'])

                # Letter Content construction
                
                # Helper to format wish with link
                def format_wish(wish, link, image_url, idx):
                    html = f"<div class='letter-wish'>To see the magic of wish #{idx}: <br>"
                    html += f"<span class='highlight-wish'>{wish}</span>"
                    if link:
                        html += f" <a href='{link}' target='_blank'>(Ver referencia 🔗)</a>"
                    
                    if image_url:
                         # We use regular st.image below, so just a marker here or we could embed img tag if we trust source
                         pass
                    html += "</div>"
                    return html

                st.markdown('<div class="letter-container">', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="letter-header">Querido Santa (osea tú, {username}) 🎅,</div>
                <div class="letter-body">
                    <p>Este año me he portado EXTRAORDINARIAMENTE bien (créeme 😉). Para esta Navidad, me haría la persona más feliz del mundo recibir alguno de estos regalitos:</p>
                    
                    <p><strong>Como primera opción (mi favorito 😍):</strong></p>
                    {format_wish(friend_info['friend_deseo1'], friend_info['friend_link_deseo1'], friend_info['friend_imagen_deseo1'], 1)}
                    
                    <p><strong>También me encantaría:</strong></p>
                    {format_wish(friend_info['friend_deseo2'], friend_info['friend_link_deseo2'], friend_info['friend_imagen_deseo2'], 2)}
                """, unsafe_allow_html=True)

                if friend_info['friend_deseo3'] != "SIN DESEO":
                    st.markdown(f"""
                    <p><strong>Y si te sientes muy generoso 😇:</strong></p>
                    {format_wish(friend_info['friend_deseo3'], friend_info['friend_link_deseo3'], friend_info['friend_imagen_deseo3'], 3)}
                    """, unsafe_allow_html=True)

                if friend_info['friend_comentarios_generales']:
                    st.markdown(f"""
                    <p><strong>P.D. (Notas importantes 📝):</strong><br>
                    {friend_info['friend_comentarios_generales']}</p>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div class="letter-footer">
                        Con cariño y esperanza,<br>
                        {friend_info['friend_character_name']} 🎄
                    </div>
                </div>
                </div>
                """, unsafe_allow_html=True)
                


                # Show images below the letter for better layout
                st.markdown("### 📸 Referencias Visuales")
                cols = st.columns(3)
                
                with cols[0]:
                    if friend_info['friend_imagen_deseo1']:
                        st.image(friend_info['friend_imagen_deseo1'], caption="Deseo #1", use_container_width=True)
                
                with cols[1]:
                    if friend_info['friend_imagen_deseo2']:
                        st.image(friend_info['friend_imagen_deseo2'], caption="Deseo #2", use_container_width=True)
                
                with cols[2]:
                    if friend_info['friend_imagen_deseo3']:
                        st.image(friend_info['friend_imagen_deseo3'], caption="Deseo #3", use_container_width=True)
            
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