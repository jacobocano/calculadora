#import streamlit as st
#st.login()
#st.write(st.query_params)

# if st.user.is_logged_in:
#     st.write(f"Sesión activa: {st.user["name"]}")
#     if st.button("Cerrar sesión"):
#         st.logout()
# else:
#     if st.button("Iniciar sesión en Microsoft"):
#         st.login("microsoftapp")
#         st.markdown(f"Welcome! {st.user["name"]} - {st.user["email"]}")
#     st.stop()

# if st.user.is_logged_in:
#     st.write(f"Sesión activa: {st.user.name}")
#     if st.button("Cerrar sesión"):
#         st.logout()
# else:
#     if st.button("Iniciar sesión en Microsoft", on_click=st.login):
#         st.login("microsoft")
#     st.stop()
#         #st.login(provider="microsoft")

# st.markdown(f"Welcome! {st.user.name} - {st.user.email}")

# def login_screen():
#     st.header("Esta es una aplicación privada.")
#     st.subheader("Por favor, inicie sesión.")
#     st.button("Iniciar sesión en Microsoft", on_click=st.login)

# if not st.user.is_logged_in:
#     login_screen()
# else:
#     st.header(f"Bienvenido, {st.user.name}!")
#     st.button("Cerrar sesión", on_click=st.logout)

# if "user" not in st.session_state:
#     st.session_state["user"] = {}

# st.button("Log out", on_click=st.logout)