import streamlit as st
import pandas as pd
import os
from openai import AzureOpenAI

# cred
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

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

    missing_columns = set(target_columns).difference(set(column_mapping.keys()))

    return column_mapping, missing_columns

column_pre_ren = None

def start_mapping():
    st.write("start mapping")
    import json
    with open("data_model.json") as f:
        target_frame = json.load(f)
    target_columns = list(target_frame['properties'].keys())
    column_pre_ren, col_massing = get_mapping(list(uploaded_df.columns), target_columns)
    st.title("Column Present or renamed")
    st.write(column_pre_ren)
    st.title("Column Missing")
    st.write(col_massing)
    return column_pre_ren

def analyse_data(df: pd.DataFrame, col_mapping: dict):
    # count how many missing values in each column
    st.title("Missing Values")
    for col in df.columns:
        nan = df[col].isna().sum()
        st.write(f"{col}: {nan}")
    # st.write(df.isna().sum())
    st.title("Missing rows")
    st.title("Change of units")
    

# Call the upload_file function in your Streamlit app
uploaded_df = upload_file()
col_map = None
if st.button("Map"):
    import time
    start_time = time.time()
    col_map = start_mapping()
    st.progress((time.time() - start_time)/60, text=f"Time taken: {round(time.time() - start_time)} seconds")

if st.button("Analyse Data"):
    st.write("Analyse Missing rows, values and column order")
    analyse_data(uploaded_df, col_map)

if st.button("Using Agent"):
    with open("agent.txt") as f:
        agent = f.read()
        st.write(agent)
