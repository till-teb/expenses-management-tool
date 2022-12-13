import os
import streamlit as st
import pandas as pd
import uuid
from user_input import store
from streamlit_function import (
    enter_data,
    delete_data,
    edit_data,
    view_data,
    remove_rows,
)

# get the right working directory
root = os.getcwd()
FILENAME = "expenses_dataset.csv"

try:
    # dataset
    file = os.path.join(root, FILENAME)
    st.session_state["df"] = pd.read_csv(file)
except:
    st.sidebar.write("No csv file found")

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
    df = st.session_state["df"]

    # add temporary unique key
    df["uuid"] = [uuid.uuid4() for _ in range(len(df.index))]

    # create a dataframe, which contain what we want to delete
    delete_df = delete_data()
    submit = st.button("Delete")
    if submit:
        st.write("Deleted successfully")
        st.write("Your old dataframe")
        st.write(df)  # old dataframe

        # delete row based on unique key
        df = remove_rows(df, "uuid", delete_df["uuid"])
        df = df.drop("uuid", axis=1)
        df.to_csv(FILENAME, index=False)  # save to the csv file
        st.write("Your new dataframe!")
        st.write(df)  # new dataframe
        st.session_state["df"] = df


if option == options[2]:
    edit_data()

if option == options[3]:
    view_data()
