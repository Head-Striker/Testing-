
import streamlit as st

st.set_page_config(
    page_title="My Website",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 Welcome to my website!")
st.write("My first website, built with Python.")

name = st.text_input("What's your name?")

if st.button("Say hello"):
    if name:
        st.success(f"Hello, {name}!")
    else:
        st.warning("Enter your name first.")

st.divider()
st.subheader("About this website")
st.write("I'm learning Python and building my own website.")
