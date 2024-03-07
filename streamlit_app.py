import streamlit as st
import pandas as pd
import os

def upload_file():
    uploaded_file = st.file_uploader("Upload a file!")
    if uploaded_file is not None:
        # Save the uploaded file name in the session state
        st.session_state.filename = uploaded_file.name
        
        # Saving the file to disk (optional, depending on your use case)
        with open(os.path.join("documents", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load the uploaded CSV into a DataFrame directly
        df = pd.read_csv(uploaded_file)
        
        # Perform operations with df here (e.g., display the DataFrame or its summary)
        st.write(df)  # This line is an example to display the DataFrame in Streamlit
        
        return df  # You can return the DataFrame if you need to use it outside this function

# Call the upload_file function in your Streamlit app
uploaded_df = upload_file()

# Now, uploaded_df contains the DataFrame loaded from the uploaded CSV file,
# and you can use it for further data analysis or visualization in your Streamlit app.
