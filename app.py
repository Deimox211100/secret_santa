import streamlit as st
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.home import HomePage
from pages.profile import ProfilePage
from pages.secret_friend import FriendPage

# Configuración de la página
st.set_page_config(
    page_title="Amigo Secreto",
    page_icon="🎄",
    initial_sidebar_state="collapsed"
)

st.navigation([st.Page("pages/home.py"), st.Page('pages/login.py') , st.Page('pages/register.py')], position="hidden", expanded=False)


# Función para establecer la página
def set_page(page_name):
    st.session_state.page = page_name
    st.rerun()


# Página inicial
def start_page():
    # Título centrado y estilizado
    st.markdown("<h1 style='text-align: center; color: white; font-size: 2.5em;'>🎄Juguemos al Amigo Secreto🎄</h1>",
                unsafe_allow_html=True)

    # Columnas para centrar la imagen
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image(
            "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmxkOWN5cHl4dTVob3p4YW52a2h4Z28yNXZ4OXZ1cnY3MW41cDF0aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/H5Ooe4b04mkawWC8KN/giphy.gif",
            use_container_width =True
        )
    with col3:
        st.write(' ')

    # Contenedor para centrar los botones
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Botones de Login y Register con estilo
        st.markdown("""
        <style>
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

        if st.button("Iniciar Sesión ➡️", use_container_width =True):
            set_page("login")
        if st.button("Registrarse 📝", use_container_width =True):
            set_page("register")


# Función principal de la aplicación
def main():
    # Configuración inicial del estado de la página
    if "page" not in st.session_state:
        st.session_state.page = "start"

    # Manejo de redirecciones basadas en el estado de sesión
    if st.session_state.page == "start":
        start_page()
    elif st.session_state.page == "login":
        login_page = LoginPage()
        login_page.run()
    elif st.session_state.page == "register":
        register_page = RegisterPage()
        register_page.run()
    elif st.session_state.page == "home":
        home_page = HomePage()
        home_page.run()
    elif st.session_state.page == "profile":
        profile_page = ProfilePage()
        profile_page.run()
    elif st.session_state.page == "secret_friend":
        friend_page = FriendPage()
        friend_page.run()


# Ejecutar la aplicación
if __name__ == "__main__":
    main()