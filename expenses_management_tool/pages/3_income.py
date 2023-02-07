import os
import numpy as np
import streamlit as st
import pandas as pd
import useful_functions as uf

# get the right working directory
root = os.getcwd()
datasets = "datasets"
FILENAME = "income_dataset.csv"

try:
    # load the dataset, if it's available
    datasets_PATH = os.path.join(root, datasets, FILENAME)
    st.session_state["income_df"] = pd.read_csv(datasets_PATH)
except:
    st.sidebar.write("No csv file found")

# page setup and description
st.title("Income")
st.subheader("Please add all your income here")


def enter_income():
    """
    Function to enter the income
    ...
    return dataframe for income
    """
    options = ["Fixed income", "Additional income"]
    categories = ["Salary", "Allowance", "Bonus", "Other"]

    option = st.selectbox("Type", options)

    # Fixed income
    if option == options[0]:
        # initiate 2 columns
        col1, col2 = st.columns(2)
        # first column content
        with col1:
            amount = st.number_input("Amount")
            DATE = np.nan
        # second column content
        with col2:
            category = st.selectbox("Category", (item for item in categories))

    # Additional income
    elif option == options[1]:
        # initiate 2 columns
        col1, col2 = st.columns(2)
        # first column content
        with col1:
            amount = st.number_input(("Amount"))
            DATE = st.date_input("Date")
        # second column content
        with col2:
            category = st.selectbox("Category", (item for item in categories))

    if "Other" in category:
        # add note option for others
        if option == options[0]:
            with col1:
                notes = st.text_input("Notes").capitalize()
                category = notes
        elif option == options[1]:
            with col2:
                notes = st.text_input("Notes").capitalize()
                category = notes

    income_df = pd.DataFrame(
        {"type": [option], "amount": [amount], "category": [category],
         "DATE": [str(DATE)]}
    )
    
    if option == options[1]:
        income_df = uf.split_DATE(income_df)
        
    income_df = income_df.drop("DATE", axis=1)
    return income_df


def store(df):
    """
    1. check if a folder for datasets already exists?
            ---> If not, create one
            ---> If yes, go into the folder directory
    2. check if a dataset already exists?
            ---> If not, create one
            ---> If yes, save the query in the dataset.
    """
    # save all the datasets into one folder "datasets"
    folder = "datasets"
    folder_PATH = os.path.join(root, folder)
    # create folder "datasets", if it's not exist
    if not os.path.exists(folder_PATH):
        os.mkdir(folder_PATH)  # create folder "datasets"
    # path to csv file in datasets folder
    datasets_PATH = os.path.join(folder_PATH, FILENAME)

    def store_in_new_ds(df):
        """
        stores the query-result in a new dataset.

        """
        data = pd.DataFrame(columns=["type", "amount", "category"])
        frames = [df, data]
        data = pd.concat(frames)
        data.to_csv(datasets_PATH, index=False)
        return data

    # check if a dataset already exist
    try:
        data = pd.read_csv(datasets_PATH)
        frames = [df, data]
        data = pd.concat(frames)
        data.to_csv(datasets_PATH, index=False)
        return data

    # if not, create one
    except:
        store_in_new_ds(df)

    return


def view_income():
    """
    Function to view the income dataframe
    Has 2 filters, which is income type and category
    ...
    return income dataframe
    """
    if "income_df" in st.session_state:
        income_df = st.session_state["income_df"]
        if len(income_df) == 0:
            st.write("No dataframe available")
        else:
            filter_prompt = st.checkbox("Use filter")
            # condition if user want to use filter
            if filter_prompt is False:
                st.write(income_df)
            else:
                options = ["Income Type", "Category"]
                # initiate container
                container = st.container()
                all = st.checkbox("Select all")
                # select all option
                if all:
                    option = container.multiselect("Filter by", options, options)
                # select some options
                else:
                    option = container.multiselect("Filter by", options)

                # only one filter is chosen
                if len(option) == 1:
                    if "Category" in option:
                        category = st.selectbox("Choose category", ("Salary", "Allowance", "Bonus", "Other"))
                        # because we dont have consistent form for others, we need to eliminate other categories
                        # for masking
                        if category == "Other":
                            remove_salary = income_df["category"] != "Salary"
                            remove_allowance = income_df["category"] != "Allowance"
                            remove_bonus = income_df["category"] != "Bonus"
                            filtered_df = income_df[remove_allowance & remove_salary & remove_bonus]
                        else:
                            mask_category = income_df["category"] == category
                            filtered_df = income_df[mask_category]

                    else:
                        income_type = st.selectbox("Choose Income Type", ("Fixed income", "Additional income"))
                        mask_type = income_df["type"] == income_type
                        filtered_df = income_df[mask_type]
                    # check if filtered_df exists
                    if len(filtered_df) != 0:
                        st.write(filtered_df)
                    else:
                        st.write("No data available")
                  
                if len(option) == 2:
                    col1, col2 = st.columns(2)
                    with col1:
                        category = st.selectbox("Choose category", ("Salary", "Allowance", "Bonus", "Other"))
                    with col2:
                        income_type = st.selectbox("Choose Income Type", ("Fixed income", "Additional income"))
                    mask_type = income_df["type"] == income_type
                    # because we dont have consistent form for others, we need to eliminate other categories
                    # for masking
                    if category == "Other":
                        remove_salary = income_df["category"] != "Salary"
                        remove_allowance = income_df["category"] != "Allowance"
                        remove_bonus = income_df["category"] != "Bonus"
                        filtered_df = income_df[remove_allowance & remove_salary & remove_bonus & mask_type]  
                    else:
                        mask_category = income_df["category"] == category
                        filtered_df = income_df[mask_category & mask_type]
                    # check if filtered_df exists
                    if len(filtered_df) != 0:
                        st.write(filtered_df)
                    else:
                        st.write("No data available")
    else:
        st.write("No dataframe available")


def delete_income():
    """
    Function to delete a single data entry from dataframe
    ...
    return a dataframe that should be deleted
    """
    # load the dataframe, if it's available
    if "income_df" in st.session_state:
        income_df = st.session_state["income_df"]
    else:
        st.write("No dataframe available")

    st.write("Do you wish to delete any data?")

    options = ["Income Type", "Category"]
    # initiate container
    container = st.container()
    all = st.checkbox("Select all")
    # select all option
    if all:
        option = container.multiselect("Filter by", options, options)
    # select some options
    else:
        option = container.multiselect("Filter by", options)

    if len(option) == 2:  # if both filter chosen
        # initiate 2 columns
        col1, col2 = st.columns(2)
        # first column content
        with col1:
            income_type = st.selectbox(
                "Choose income type", ("Fixed Income", "Additional Income")
            )

        # second column content
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

    # if no filter is chosen
    elif len(option) == 0:
        filtered_df = income_df  # return df without filter
        st.write("No filter is chosen")
        st.write(filtered_df)

    # check if filtered_df exist
    if len(filtered_df) != 0:
        delete_index = st.multiselect(
            "Choose index to delete", (filtered_df.index.values)
        )
        delete_df = filtered_df.iloc[delete_index]
        st.write("This entry will be deleted")
        if len(delete_df) == 0:
            st.write("No data is chosen ")
        else:
            st.write(delete_df)
        return delete_df


# main menu option
options = ["Add income", "Delete income", "View your dataframe"]

option = st.selectbox("What you want to do", (item for item in options))

if option == options[0]:
    docs = """
    Add single entry option:
        1. Create a new dataframe from the new entry
        2. Simple input check for new entry
            - if "amount" is not None, then proceed to next step
            - if "amount" is None, notify as invalid input
        3. Store the new dataframe
            - if no dataframe available, create new one
            - if dataframe already exist, merge with new dataframe and save it
        4. Load it into session_state
    """
    income_df = enter_income()  # 1
    submit = st.button("Submit")
    if submit:
        if income_df["amount"][0] != 0:  # 2
            income_df = store(income_df)  # 3
            st.session_state["income_df"] = income_df  # 4
            st.write("Saved successfully")
        else:
            st.write("Invalid input")

elif option == options[1]:
    docs = """
    Delete entry option:
        1. Load the dataframe from the session_state, if it's available
        2. Create a dataframe, which contain what user want to delete
        3. Simple input check for delete_df, if it's exist
        4. Delete row from dataframe based on index delete_df
        5. Save to csv file
    """
    if "income_df" in st.session_state:
        # 1
        income_df = st.session_state["income_df"]
        # 2
        delete_df = delete_income()
        # 3
        if delete_df is not None:
            submit = st.button("Delete")
            if submit:
                st.write("Deleted successfully")
                # 4
                income_df = income_df.drop(index=delete_df.index.values, axis=1)
                # 5
                income_df.to_csv(datasets_PATH, index=False)
                st.info("Your new dataframe!", icon="ℹ️")
                if len(income_df) == 0:
                    st.write("No dataframe available")
                else:
                    st.write(income_df)  # new dataframe
                    # save it again in session state
                st.session_state["income_df"] = income_df
    else:
        st.write("No dataframe available")

elif option == options[2]:
    view_income()
