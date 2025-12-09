import streamlit as st
import os
from dotenv import load_dotenv
import subprocess
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.supabase_client import get_supabase_client
from utils.email_sender import send_email, EmailConfigError

# Load environment variables
load_dotenv()


class AdminPage:
    def __init__(self):
        # Get Supabase client
        self.supabase = get_supabase_client()

        # CSS para estilos personalizados
        st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
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
        .admin-button {
            background-color: #FF6B6B !important;
        }
        .admin-button:hover {
            background-color: #FF5252 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    def get_stats(self):
        """Get statistics about users and assignments."""
        try:
            # Count total users
            users_response = self.supabase.table('users').select('*', count='exact').execute()
            total_users = users_response.count if users_response.count is not None else len(users_response.data)
            
            # Count assigned friends
            friends_response = self.supabase.table('secret_friends').select('*', count='exact').execute()
            total_assignments = friends_response.count if friends_response.count is not None else len(friends_response.data)
            
            # Check if wishes are locked
            # We check the first user as the lock status is global (applied to all users)
            lock_response = self.supabase.table('users').select('wishes_locked').limit(1).execute()
            wishes_locked = False
            if lock_response.data and len(lock_response.data) > 0:
                wishes_locked = lock_response.data[0]['wishes_locked']
            
            return {
                'total_users': total_users,
                'total_assignments': total_assignments,
                'wishes_locked': wishes_locked
            }
        except Exception as e:
            st.error(f"Error fetching stats: {e}")
            return None

    def assign_friends(self):
        """Run the assign_friends.py script."""
        # Note: assign_friends.py might need to be updated to use Supabase API as well
        # For now, we'll assume it's updated or we should update it.
        # Given the user request, we should probably update it too, but let's stick to the pages first.
        try:
            result = subprocess.run(
                ['python3', 'utils/assign_friends.py'],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(__file__))
            )
            if result.returncode == 0:
                st.success("✅ Amigos secretos asignados exitosamente!")
                return True
            else:
                st.error(f"❌ Error al asignar amigos: {result.stderr}")
                return False
        except Exception as e:
            st.error(f"❌ Error ejecutando script: {e}")
            return False

    def toggle_wishes_lock(self, lock: bool):
        """Lock or unlock wishes editing for all users."""
        try:
            # Update all users
            # Supabase update without where clause is blocked by default for safety
            # But we can use a condition that is always true or iterate
            # Or better, we can use a specific RPC function if we had one.
            # For now, let's try to update where id > 0 which should cover all users
            response = self.supabase.table('users').update({'wishes_locked': lock}).gt('id', 0).execute()
            
            if response.data:
                status = "bloqueados" if lock else "desbloqueados"
                st.success(f"✅ Deseos {status} exitosamente!")
                return True
            return False
        except Exception as e:
            st.error(f"Error updating wishes lock: {e}")
            return False

    def build_letter_html(self, santa_name: str, friend: dict) -> str:
        """Build the HTML body for the secret friend wishes letter."""
        # Helper to format each wish block
        def format_wish(wish: str, link: str | None, idx: int) -> str:
            if not wish:
                return ""
            html = f"<div style='margin-left:20px;margin-bottom:15px;'>"
            html += f"Para ver la magia del deseo #{idx}:<br>"
            html += f"<span style='color:#c0392b;font-weight:bold;'>{wish}</span>"
            if link:
                html += f" <a href='{link}' target='_blank' style='color:#d35400;text-decoration:none;'>(Ver referencia 🔗)</a>"
            html += "</div>"
            return html

        wishes_html = ""
        wishes_html += "<p><strong>Como primera opción (mi favorito 😍):</strong></p>"
        wishes_html += format_wish(friend.get("friend_deseo1", ""), friend.get("friend_link_deseo1"), 1)

        wishes_html += "<p><strong>También me encantaría:</strong></p>"
        wishes_html += format_wish(friend.get("friend_deseo2", ""), friend.get("friend_link_deseo2"), 2)

        if friend.get("friend_deseo3") and friend.get("friend_deseo3") != "SIN DESEO":
            wishes_html += "<p><strong>Y si te sientes muy generoso 😇:</strong></p>"
            wishes_html += format_wish(friend.get("friend_deseo3", ""), friend.get("friend_link_deseo3"), 3)

        comentarios = ""
        if friend.get("friend_comentarios_generales"):
            comentarios = (
                "<p><strong>P.D. (Notas importantes 📝):</strong><br>"
                f"{friend['friend_comentarios_generales']}</p>"
            )

        html = f"""
        <div style="background-color:#f8f9fa;color:#2c3e50;padding:40px;border-radius:10px;
                    font-family:'Courier New',Courier,monospace;line-height:1.6;
                    box-shadow:0 4px 8px rgba(0,0,0,0.1);border:2px solid #e0e0e0;">
            <div style="font-size:1.5em;font-weight:bold;margin-bottom:20px;">
                Querido Santa (osea tú, {santa_name}) 🎅,
            </div>
            <div style="font-size:1.2em;">
                <p>Este año me he portado EXTRAORDINARIAMENTE bien (créeme 😉).
                Para esta Navidad, me haría la persona más feliz del mundo recibir
                alguno de estos regalitos:</p>
                {wishes_html}
                {comentarios}
                <div style="margin-top:40px;text-align:right;font-size:1.3em;font-style:italic;">
                    Con cariño y esperanza,<br>
                    {friend.get('friend_character_name', '')} 🎄
                </div>
            </div>
        </div>
        """
        return html

    def send_wishes_emails(self):
        """Send secret friend wishes by email to all users with assignments.

        For each record in secret_friends, the user (Santa) receives an email
        with the wishes of their assigned friend.
        """
        try:
            assignments_resp = self.supabase.table('secret_friends').select('user_id, id_secret_friend').execute()
        except Exception as e:
            st.error(f"Error obteniendo asignaciones: {e}")
            return 0, 0

        assignments = assignments_resp.data or []
        if not assignments:
            st.info("No hay asignaciones de Amigo Secreto para enviar.")
            return 0, 0

        sent_ok = 0
        sent_error = 0

        for row in assignments:
            user_id = row.get('user_id')
            friend_id = row.get('id_secret_friend')
            if user_id is None or friend_id is None:
                continue

            try:
                # Get Santa (recipient) info
                santa_resp = self.supabase.table('users').select('email, character_name').eq('id', user_id).execute()
                if not santa_resp.data:
                    continue
                santa = santa_resp.data[0]
                to_email = santa.get('email')
                santa_name = santa.get('character_name') or santa.get('nombre', '')
                if not to_email:
                    continue

                # Get friend (wishes owner) info
                friend_resp = self.supabase.table('users').select(
                    'character_name, deseo1, link_deseo1, '
                    'deseo2, link_deseo2, deseo3, link_deseo3, comentarios_generales'
                ).eq('id', friend_id).execute()

                if not friend_resp.data:
                    continue

                friend_row = friend_resp.data[0]
                friend_info = {
                    'friend_character_name': friend_row.get('character_name', ''),
                    'friend_deseo1': friend_row.get('deseo1', ''),
                    'friend_link_deseo1': friend_row.get('link_deseo1', ''),
                    'friend_deseo2': friend_row.get('deseo2', ''),
                    'friend_link_deseo2': friend_row.get('link_deseo2', ''),
                    'friend_deseo3': friend_row.get('deseo3', ''),
                    'friend_link_deseo3': friend_row.get('link_deseo3', ''),
                    'friend_comentarios_generales': friend_row.get('comentarios_generales', ''),
                }

                html_body = self.build_letter_html(santa_name, friend_info)
                subject = f"🎅 Carta de tu Amigo Secreto - {friend_info['friend_character_name']}"

                # Simple text version
                text_body = (
                    f"Hola {santa_name},\n\n"
                    f"Tu Amigo Secreto es: {friend_info['friend_character_name']}.\n"
                    "Revisa la versión HTML de este correo para ver la carta completa y los detalles de los deseos.\n\n"
                    "¡Felices fiestas!"
                )

                send_email(to_email, subject, html_body, text_body)
                sent_ok += 1
            except EmailConfigError as e:
                st.error(f"Error de configuración de correo: {e}")
                return sent_ok, sent_error
            except Exception as e:  # noqa: BLE001
                sent_error += 1
                st.warning(f"No se pudo enviar el correo a usuario {user_id}: {e}")

        return sent_ok, sent_error

    def render_dashboard(self):
        """Render the admin dashboard."""
        st.markdown("<h1 style='text-align: center; color: white;'>🔐 Panel de Administrador</h1>",
                    unsafe_allow_html=True)

        # Get statistics
        stats = self.get_stats()
        
        if stats:
            # Display stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("👥 Usuarios Registrados", stats['total_users'])
            with col2:
                st.metric("🎁 Asignaciones", stats['total_assignments'])
            with col3:
                lock_status = "🔒 Bloqueados" if stats['wishes_locked'] else "🔓 Desbloqueados"
                st.metric("Deseos", lock_status)

            st.markdown("---")

            # Admin actions
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎲 Asignar Amigos Secretos")
                st.write("Ejecuta el sorteo y asigna un amigo secreto a cada participante.")
                
                if st.button("🎲 Ejecutar Sorteo", use_container_width=True, type="primary"):
                    with st.spinner("Asignando amigos secretos..."):
                        self.assign_friends()
                        st.rerun()

            with col2:
                st.subheader("🔒 Control de Deseos")
                st.write("Bloquea o desbloquea la edición de deseos de los usuarios.")
                
                if stats['wishes_locked']:
                    if st.button("🔓 Desbloquear Deseos", use_container_width=True):
                        self.toggle_wishes_lock(False)
                        st.rerun()
                else:
                    if st.button("🔒 Bloquear Deseos", use_container_width=True):
                        self.toggle_wishes_lock(True)
                        st.rerun()

            st.markdown("---")

            st.subheader("📧 Enviar cartas por correo")
            st.write("Envía a cada participante la carta de deseos de su Amigo Secreto por correo electrónico.")

            if st.button("📧 Enviar todas las cartas", use_container_width=True):
                with st.spinner("Enviando cartas a todos los participantes..."):
                    enviados, errores = self.send_wishes_emails()
                st.success(f"Correos enviados correctamente: {enviados}")
                if errores:
                    st.warning(f"No se pudieron enviar {errores} correos. Revisa los detalles en los mensajes de arriba.")

        st.markdown("---")
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.is_admin = False
            st.session_state.username = None
            st.session_state.page = "start"
            st.rerun()

    def run(self):
        """Run the admin dashboard."""
        # Check if user is admin
        if 'is_admin' not in st.session_state or not st.session_state.is_admin:
            st.error("⛔ Acceso denegado. Solo administradores.")
            if st.button("Volver"):
                st.session_state.page = "start"
                st.rerun()
        else:
            self.render_dashboard()


def main():
    app = AdminPage()
    app.run()


if __name__ == "__main__":
    main()
