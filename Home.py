import streamlit as st
from Pages.Preprocessing import preprocess_app

def main():
    st.sidebar.title("Navigation")
    pages = ["Home"]
    selected_page = st.sidebar.selectbox("Select Page", pages)

    if selected_page == "Home":
        preprocess_app()

if __name__ == "__main__":
    main()
