import os
import streamlit as st
import pandas as pd
import uuid


# get the right working directory
root = os.getcwd()
FILENAME = "recurring_expenses.csv"

# load the dataset
file = os.path.join(root, FILENAME)

try:
    # dataset
    file = os.path.join(root, FILENAME)
    st.session_state["recurring_df"] = pd.read_csv(file)
except:
    st.sidebar.write("No csv file found")

# page title and description
st.title("Recurring expense")
st.subheader("Please add your monthly fixed cost / commitment here")

# define the categories
categories = [
    "Consumables",
    "Food & Beverages",
    "Leisure & Entertainment",
    "Transportation",
    "Other & Extraordinary",
]

# define the subcategories
subcategories = [
    [
        "Clothing",
        "Drugstore",
        "Education",
        "Electronics",
        "Furniture",
        "Medicines",
        "Narcotics",
        "Pets",
        "Stationery",
        "Other",
    ],
    ["Bakery", "Kiosk", "Market", "Supermarket", "Other"],
    [
        "Cinema",
        "Event",
        "Hairdresser",
        "Hobby",
        "Party",
        "Restaurant",
        "Vacation",
        "Other",
    ],
    ["Public transportation", "Private transportation", "Other"],
    ["Additional costs", "Investment", "Other"],
]


def enter_recurring():
    """
    Function to add recurring expense
    ...
    return a dataframe
    """
    # initiate 2 container side by side
    col1, col2 = st.columns(2)
    # first column content
    with col1:
        item = st.text_input("Item")
        amount = st.number_input("Price")
        importance = st.slider("Importance scale", min_value=1, max_value=4)

    # second column content
    with col2:
        category = st.selectbox("Category", (item for item in categories))

        # show subcategories related to its main category
        if category == categories[0]:
            subcategory = st.selectbox(
                "Subcategory", (item for item in subcategories[0])
            )

        elif category == categories[1]:
            subcategory = st.selectbox(
                "Subcategory", (item for item in subcategories[1])
            )

        elif category == categories[2]:
            subcategory = st.selectbox(
                "Subcategory", (item for item in subcategories[2])
            )

        elif category == categories[3]:
            subcategory = st.selectbox(
                "Subcategory", (item for item in subcategories[3])
            )

        elif category == categories[4]:
            subcategory = st.selectbox(
                "Subcategory", (item for item in subcategories[4])
            )

    recurring_df = pd.DataFrame(
        {
            "item": [item],
            "amount": [amount],
            "importance": [importance],
            "category": [category],
            "subcategory": [subcategory],
        }
    )
    return recurring_df


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
        data = pd.DataFrame(
            columns=["item", "amount", "importance", "category", "subcategory"]
        )
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


def delete_recurring():
    """
    Function to delete a single data entry from recurring dataframe
    ...
    return a dataframe that should be deleted
    """
    # load the dataframe, if it's available
    if "recurring_df" in st.session_state:
        df = st.session_state["recurring_df"]
    else:
        st.write("No dataframe available")

    st.write("Do you wish to delete any data?")

    options = ["Category", "Importance"]
    # initiate container
    container = st.container()
    all = st.checkbox("Select all")
    # select all option
    if all:
        option = container.multiselect("Filter by", options, options)
    # select some options
    else:
        option = container.multiselect("Filter by", options)

    if len(option) == 2:
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Choose category", (item for item in categories))

        with col2:
            importance = st.selectbox("Choose importance", (i for i in range(1, 5)))

        mask_cat = df["category"] == category
        mask_imp = df["importance"] == importance
        filtered_df = df[mask_cat & mask_imp]
        if len(filtered_df) == 0:
            st.write("No data available")
        else:
            st.write(filtered_df)

    elif "Category" in option:
        category = st.selectbox("Choose category", (item for item in categories))
        mask = df["category"] == category
        filtered_df = df[mask]
        if len(filtered_df) == 0:
            st.write("No data available")
        else:
            st.write(filtered_df)

    elif "Importance" in option:
        importance = st.selectbox("Choose importance", (i for i in range(1, 5)))
        mask = df["importance"] == importance
        filtered_df = df[mask]
        if len(filtered_df) == 0:
            st.write("No data available")
        else:
            st.write(filtered_df)

    try:
        # check if filtered_df exist
        if len(filtered_df) != 0:
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


def view_recurring():
    """
    Function to view the dataframe
    """
    if "recurring_df" in st.session_state:
        recurring_df = st.session_state["recurring_df"]
        if len(recurring_df) == 0:
            st.write("No dataframe available")
        else:
            st.write(recurring_df)
    else:
        st.write("No dataframe available")


# main menu option
options = ["Add single entry", "Delete entry", "View your dataframe"]

option = st.selectbox("What you want to do", (item for item in options))

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
    recurring_df = enter_recurring()  # 1
    submit = st.button("Submit")
    if submit:
        if recurring_df["item"][0] != "":  # 2
            recurring_df = store(recurring_df)  # 3
            st.session_state["recurring_df"] = recurring_df  # 4
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
        recurring_df = st.session_state["recurring_df"]
        # 2
        recurring_df["uuid"] = [uuid.uuid4() for _ in range(len(recurring_df.index))]
        # 3
        delete_df = delete_recurring()
        # 4
        if delete_df is not None:
            submit = st.button("Delete")
            if submit:
                st.write("Deleted successfully")
                st.write("Your old dataframe")
                st.write(recurring_df)  # old dataframe
                # 5
                recurring_df = remove_rows(recurring_df, "uuid", delete_df["uuid"])
                recurring_df = recurring_df.drop("uuid", axis=1)
                # 6
                recurring_df.to_csv(FILENAME, index=False)
                st.write("Your new dataframe!")
                if len(recurring_df) == 0:
                    st.write("No dataframe available")
                else:
                    st.write(recurring_df)  # new dataframe

                    # save it again in session_state
                    st.session_state["recurring_df"] = recurring_df
    except:
        st.write("No dataframe available")

if option == options[2]:
    view_recurring()
