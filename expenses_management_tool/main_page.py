import os
import streamlit as st
import pandas as pd
from user_input import store
from streamlit_function import enter_data, delete_data, edit_data, view_data

# get the right working directory
root = os.getcwd()
FILENAME = "expenses_dataset.csv"

# dataset
file = os.path.join(root, FILENAME)

st.session_state["df"] = pd.read_csv(file)

st.title("Expenses")
# st.write("What are you spend?")


options = ["Enter single entry", "Delete entry", "Edit entry", "View your dataframe"]

# Create a select box
option = st.selectbox("What you want to do", options)

if option == options[0]:
    df = enter_data()
    submit = st.button("submit")
    if submit:
        if df["item"][0] != "":  # check input for item
            df = store(df)  # save as csv in datasets folder
            st.session_state["df"] = df
            st.write("Saved successfully")
        else:
            st.write("Invalid input")


if option == options[1]:
    delete_data()

if option == options[2]:
    edit_data()

if option == options[3]:
    view_data()
