import streamlit as st


class HomePage:
    def __init__(self):
        # Aplicar estilos CSS personalizados
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
        .title {
            text-align: center;
            color: white;
            font-size: 3em;
            margin-bottom: 30px;
        }
        </style>
        """, unsafe_allow_html=True)

    def render_home_page(self):
        """Renderizar la página de inicio."""
        # Título principal
        st.markdown("<h1 class='title'>🎄 Juguemos al Amigo Secreto 🎄</h1>", unsafe_allow_html=True)

        # Columnas para centrar los botones
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Verificar si el usuario está autenticado
            if 'logged_in' not in st.session_state or not st.session_state.logged_in:
                # Mostrar imagen principal solo si NO está logueado
                st.image(
                    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdzBoZWhsNjBhMnBleTIxdnJoczd5ZW05d2JiYjZmeTFqbHUxNm5pMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HBMCmtsPEUShG/giphy.gif",
                    use_container_width=True
                )
                
                # Botones de Login y Register
                if st.button("Iniciar Sesión ➡️", use_container_width=True):
                    st.session_state.page = "login"
                    st.rerun()

                if st.button("Registrarse 📝", use_container_width=True):
                    st.session_state.page = "register"
                    st.rerun()

                if st.button("Olvidé mi personaje 🔍", use_container_width=True):
                    st.session_state.page = "recover"
                    st.rerun()

                if st.button("Cambiar Contraseña 🔄", use_container_width=True):
                    st.session_state.page = "change_password"
                    st.rerun()
            else:
                # Si el usuario está logueado, mostrar opciones adicionales
                st.markdown(
                    f"<h2 style='text-align: center; color: white;'>¡Bienvenid@ {st.session_state.username}!</h2>",
                    unsafe_allow_html=True)
                
                # Mostrar imagen del personaje si existe (centrada)
                if 'character_photo_url' in st.session_state and st.session_state.character_photo_url:
                    sub_col1, sub_col2, sub_col3 = st.columns([1, 2, 1])
                    with sub_col2:
                        st.image(st.session_state.character_photo_url, use_container_width=True, caption=st.session_state.username)

                if st.button("Ver Mi Perfil", use_container_width=True):
                    # Aquí podrías agregar la navegación a la página de perfil
                    st.session_state.page = "profile"
                    st.rerun()

                if st.button("Ver Amigo Secreto", use_container_width=True):
                    # Aquí podrías agregar la navegación a la página de participantes
                    st.session_state.page = "secret_friend"
                    st.rerun()

                if st.button("Cerrar Sesión", use_container_width=True):
                    # Limpiar el estado de sesión
                    st.session_state.logged_in = False
                    st.session_state.username = None
                    st.session_state.page = "start"
                    st.rerun()

    def run(self):
        """Ejecutar la página de inicio."""
        self.render_home_page()


def main():
    home_page = HomePage()
    home_page.run()


if __name__ == "__main__":
    main()