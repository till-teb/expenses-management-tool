import os
import streamlit as st
import pandas as pd
import uuid
from useful_functions import store
import streamlit_function as sf
# get the right working directory
root = os.getcwd()
datasets = "datasets"
FILENAME = "expenses_dataset.csv"

try:
    # load the dataset, if it's available
    datasets_PATH = os.path.join(root, datasets, FILENAME)
    st.session_state["df"] = pd.read_csv(datasets_PATH)
except:
    st.sidebar.write("No csv file found")

# page title and its subheader
st.title("Expenses")
st.subheader("Please add all your expenses here")


options = ["Add single entry", "Delete entry", "View your dataframe"]

# Create a select box, to choose an option from options
option = st.selectbox("What you want to do", options)

if option == options[0]:
    docs = """
    Add single entry option:
        1. Create a new dataframe from the new entry
        2. Simple input check for new entry
            - if "item" is not None, then proceed to next step
            - if "item" is None, notify as invalid input
        3. Store the new dataframe
            - if no dataframe available, create new one
            - if dataframe already exist, merge with new dataframe and save it
        4. Load it into session_state
    """
    # 1
    df = sf.enter_data()
    submit = st.button("submit")
    if submit:
        # 2
        if df["item"][0] != "":
            # 3
            df = store(df)
            # 4
            st.session_state["df"] = df
            st.write("Saved successfully")
        else:
            st.write("Invalid input")


if option == options[1]:
    docs = """
    Delete entry option:
        1. Load the dataframe from the session_state, if it's available
        2. Assign temporary unique key to the dataframe
        3. Create a dataframe, which contain what user want to delete
        4. Simple input check for delete_df, if it's exist
        5. Delete row from dataframe based on unique key.
        6. Save to csv file
    """
    try:
        # 1
        df = st.session_state["df"]
        # 2
        df["uuid"] = [uuid.uuid4() for _ in range(len(df.index))]
        # 3
        delete_df = sf.delete_data()
        # 4
        if delete_df is not None:
            submit = st.button("Delete")
            if submit:
                st.write("Deleted successfully")
                st.write("Your old dataframe")
                st.write(df)  # old dataframe
                # 5
                df = sf.remove_rows(df, "uuid", delete_df["uuid"])
                df = df.drop("uuid", axis=1)
                # 6
                df.to_csv(datasets_PATH, index=False)
                st.write("Your new dataframe!")
                if len(df) == 0:
                    st.write("No dataframe available")
                else:
                    st.write(df)  # new dataframe
                st.session_state["df"] = df
    except:
        st.write("No dataframe available")


if option == options[2]:
    # Show the dataframe, if it's available
    sf.view_data()
