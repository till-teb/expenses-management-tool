import os
import numpy as np
import streamlit as st
import pandas as pd
import uuid

# get the right working directory
root = os.getcwd()
FILENAME = "income_dataset.csv"

# dataset
file = os.path.join(root, FILENAME)

try:
    # load the dataset
    file = os.path.join(root, FILENAME)
    st.session_state["income_df"] = pd.read_csv(file)
except:
    st.sidebar.write("No csv file found")

# page setup and description
st.title("Income")
st.subheader("Please enter all your income here")


def enter_income():
    """
    Function to enter the income

    return dataframe for income
    """
    options = ["Fixed income", "Additional income"]
    categories = ["Salary", "Allowance", "Bonus", "Other"]

    option = st.selectbox("Type", options)

    if option == options[0]:
        # create container side by side
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Amount")
        with col2:
            category = st.selectbox("Category", (item for item in categories))

    elif option == options[1]:
        # create container side by side
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input(("Amount"))
        with col2:
            category = st.selectbox("Category", (item for item in categories))

    if "Other" in category:
        with col1:
            notes = st.text_input("Notes")

    else:
        notes = np.nan

    income_df = pd.DataFrame(
        {"type": [option], "amount": [amount], "category": [category], "notes": [notes]}
    )
    return income_df


def store(df):
    """
    check if a dataset already exists?

            ---> If not, create one

            ---> If yes, save the query in the dataset.
    """

    def store_in_new_ds(df):
        """
        stores the query-result in a new dataset.

        """
        data = pd.DataFrame(columns=["type", "amount", "category", "notes"])
        frames = [df, data]
        data = pd.concat(frames)

        # save all the datasets into one folder "datasets"
        # folder = "datasets"
        # folder_PATH = os.path.join(root, folder)
        # if not os.path.exists(folder_PATH):
        #     os.mkdir(folder_PATH)  # create folder "datasets"

        data.to_csv(FILENAME, index=False)
        return data

    # check if a dataset already exist
    try:
        data = pd.read_csv(file)
        frames = [df, data]
        data = pd.concat(frames)
        data.to_csv(FILENAME, index=False)
        return data

    # if not, create one
    except:
        store_in_new_ds(df)

    return


def view_income():
    """
    Function to view the income dataframe
    return income dataframe
    """
    if "income_df" in st.session_state:
        income_df = st.session_state["income_df"]
        if len(income_df) == 0:
            st.write("No dataframe available")
        else:
            st.write(income_df)
    else:
        st.write("No dataframe available")


def delete_income():
    """
    Function to delete a single data entry from dataframe
    """
    if "income_df" in st.session_state:
        income_df = st.session_state["income_df"]
    else:
        st.write("No dataframe available")

    st.write("Do you wish to delete any data?")

    options = ["Income Type", "Category"]
    option = st.multiselect("Filter by", options)

    if len(option) == 2:
        col1, col2 = st.columns(2)
        with col1:
            income_type = st.selectbox(
                "Choose income type", ("Fixed Income", "Additional Income")
            )

        with col2:
            category = st.selectbox(
                "Choose category", ("Salary", "Allowance", "Bonus", "Other")
            )

        mask_cat = income_df["category"] == category
        mask_type = income_df["type"] == income_type
        filtered_df = income_df[mask_cat & mask_type]
        if len(filtered_df) == 0:
            st.write("No data available")
        else:
            st.write(filtered_df)

    elif "Category" in option:
        category = st.selectbox(
            "Choose category", ("Salary", "Allowance", "Bonus", "Other")
        )
        mask = income_df["category"] == category
        filtered_df = income_df[mask]
        if len(filtered_df) == 0:
            st.write("No data available")
        else:
            st.write(filtered_df)

    elif "Income Type" in option:
        income_type = st.selectbox(
            "Choose income type", ("Fixed income", "Additional income")
        )
        mask = income_df["type"] == income_type
        filtered_df = income_df[mask]
        if len(filtered_df) == 0:
            st.write("No data available")
        else:
            st.write(filtered_df)

    try:
        delete_index = st.multiselect(
            "Choose index to delete", (i for i in range(0, len(filtered_df)))
        )
        delete_df = filtered_df.iloc[delete_index]
        st.write("This entry will be deleted")
        if len(delete_df) == 0:
            st.write("No data is chosen ")
        else:
            st.write(delete_df)
        return delete_df

    except:
        st.write("Please choose your filter")


def remove_rows(df, col, values):
    """
    Function to remove row from selected column, that contain values.
    Values can be a list.
    """
    return df[~df[col].isin(values)]


# main menu option
options = ["Add income", "Delete income", "View your dataframe"]

option = st.selectbox("What you want to do", (item for item in options))

if option == options[0]:
    income_df = enter_income()
    submit = st.button("Submit")
    if submit:
        if income_df["amount"][0] != 0:  # check input for amount
            income_df = store(income_df)  # save the income
            st.session_state["income_df"] = income_df
            st.write("Saved successfully")
        else:
            st.write("Invalid input")

elif option == options[1]:
    # load the file from cache
    income_df = st.session_state["income_df"]

    # add temporary unique key
    income_df["uuid"] = [uuid.uuid4() for _ in range(len(income_df.index))]

    # create a dataframe, which contain what we want to delete
    delete_df = delete_income()
    if delete_df is not None:
        submit = st.button("Delete")
        if submit:
            st.write("Deleted successfully")
            st.write("Your old dataframe")
            st.write(income_df)  # old dataframe

            # delete row based on unique key
            income_df = remove_rows(income_df, "uuid", delete_df["uuid"])
            income_df = income_df.drop("uuid", axis=1)
            income_df.to_csv(FILENAME, index=False)  # save to the csv file
            st.write("Your new dataframe!")
            if len(income_df) == 0:
                st.write("No dataframe available")
            else:
                st.write(income_df)  # new dataframe

                # save it again in cache
                st.session_state["income_df"] = income_df

elif option == options[2]:
    view_income()
