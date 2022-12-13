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
st.subheader("Here is your monthly fixed cost / your monthly commitment")

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
    col1, col2 = st.columns(2)
    with col1:
        item = st.text_input("Item")
        amount = st.number_input("Price")
        importance = st.slider("Importance scale", min_value=1, max_value=4)

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
    Function to delete a single data entry from dataframe
    """
    if "recurring_df" in st.session_state:
        df = st.session_state["recurring_df"]
    else:
        st.write("No dataframe available")

    st.write("Do you wish to delete any data?")

    options = ["Category", "Importance"]
    option = st.multiselect("Filter by", options)

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
options = ["Enter single entry", "Delete entry", "View your dataframe"]

option = st.selectbox("What you want to do", (item for item in options))

if option == options[0]:
    recurring_df = enter_recurring()
    submit = st.button("Submit")
    if submit:
        if recurring_df["item"][0] != "":  # check input for item
            recurring_df = store(recurring_df)
            st.session_state["recurring_df"] = recurring_df
            st.write("Saved successfully")
        else:
            st.write("Invalid input")


if option == options[1]:
    # load the file from cache
    recurring_df = st.session_state["recurring_df"]

    # add temporary unique key
    recurring_df["uuid"] = [uuid.uuid4() for _ in range(len(recurring_df.index))]

    # create a dataframe, which contain what we want to delete
    delete_df = delete_recurring()
    if delete_df is not None:
        submit = st.button("Delete")
        if submit:
            st.write("Deleted successfully")
            st.write("Your old dataframe")
            st.write(recurring_df)  # old dataframe

            # delete row based on unique key
            recurring_df = remove_rows(recurring_df, "uuid", delete_df["uuid"])
            recurring_df = recurring_df.drop("uuid", axis=1)
            recurring_df.to_csv(FILENAME, index=False)  # save to the csv file
            st.write("Your new dataframe!")
            if len(recurring_df) == 0:
                st.write("No dataframe available")
            else:
                st.write(recurring_df)  # new dataframe
                
                # save it again in cache
                st.session_state["recurring_df"] = recurring_df  

if option == options[2]:
    view_recurring()
