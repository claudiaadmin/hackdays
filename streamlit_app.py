import streamlit as st
import pandas as pd
import os
from openai import AzureOpenAI
import time

client = AzureOpenAI(
    api_version="2024-02-15-preview",
    # azure_deployment="gpt-vision",
    azure_deployment="gpt4genwizard",
    max_retries=3,
)

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

def get_mapping(m_columns: list, target_columns: list) -> dict:
    # inputs: lists of column names
    # output: dict of mapping

    messages = [
        {
            "role": "user",
            "content": f"I have two lists with column names. These names need to be mapped 1 on 1. Can you do this mapping? Please just answer in a format like column1: column2 etc. Please do not make any additional notes. The first list is {m_columns}, the second list is {list(set(target_columns))}"
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5",
        messages=messages
    )

    split_list = [x.split(': ') for x in response.choices[0].message.content.split('\n')]
    column_mapping = {x[0]: x[1] for x in split_list}

    if min([len(m_columns), len(target_columns)]) != len(column_mapping):
        print(f'length of machine: {len(m_columns)}, length of target columns: {len(target_columns)}, length of mapping: {len(column_mapping)}')

    return column_mapping

def start_mapping():
    st.write("start mapping")
    import json
    with open("data_model.json") as f:
        target_frame = json.load(f)
    target_columns = list(target_frame['properties'].keys())
    rst = get_mapping(list(uploaded_df.columns), target_columns)
    
# Call the upload_file function in your Streamlit app
uploaded_df = upload_file()

if st.button("Map"):
    start_mapping()



