import streamlit as st
import pandas as pd
 
st.write("""
# My first app
Hello *world!*
""")


def upload_file():
    uploaded_file = st.file_uploader("Upload a file!")
    if uploaded_file is not None:
        st.session_state.filename = uploaded_file.name
        with open(os.path.join("documents", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
