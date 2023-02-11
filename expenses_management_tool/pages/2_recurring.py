import os
import streamlit as st
import pandas as pd
import streamlit_function as sf

# get the right working directory
root = os.getcwd()
datasets = "datasets"
FILENAME = "recurring_expenses.csv"

try:
    # load the datasets, if it's available
    datasets_PATH = os.path.join(root, datasets, FILENAME)
    st.session_state["recurring_df"] = pd.read_csv(datasets_PATH)
except:
    st.sidebar.write("No csv file found")

# page title and description
st.title("Fix expenses")
st.subheader("Please add your monthly fixed cost / commitment here")

# define the categories
categories = [
    "Consumables",
    "Food & Beverages",
    "Leisure & Entertainment",
    "Transportation",
    "Other & Extraordinary",
    "Financial Fees",
    "Living Area"
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
    ["Public Transportation", "Private Transportation", "Other"],
    ["Additional Costs", "Investment", "Other"],
    ["Taxes", "Insurance", "Bank", "Other"],
    ["Energy", "Rent","Household Appliances ","Decoration", "Other"]
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
        item = st.text_input("Item").capitalize()
        amount = st.number_input("Price")
        importance_dict = {"Not important" : 1,
                           "Less Important" : 2,
                           "Important" : 3,
                           " Most Important" : 4}
        importance_word = st.select_slider("Importance scale", (i for i in importance_dict.keys()))
        importance = importance_dict.get(importance_word)

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
        elif category == categories[5]:
            subcategory = st.selectbox(
                "Subcategory", (item for item in subcategories[5])
            )
        elif category == categories[6]:
            subcategory = st.selectbox(
                "Subcategory", (item for item in subcategories[6])
            )

        if subcategory == "Other":
            notes = st.text_input("Notes").capitalize()
            subcategory = notes

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
        os.mkdir(folder_PATH)
    # path to csv file in datasets folder
    datasets_PATH = os.path.join(folder_PATH, FILENAME)

    def store_in_new_ds(df):
        """
        stores the query-result in a new dataset.

        """
        data = pd.DataFrame(
            columns=["item", "amount", "importance", "category", "subcategory"]
        )
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

    # if no filter is chosen
    elif len(option) == 0:
        filtered_df = recurring_df  # return df without filter
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


def view_recurring():
    """
    Function to view the dataframe
    Has 2 filters, which is category and importance
    ...
    return recurrinf dataframe
    """
    if "recurring_df" in st.session_state:
        recurring_df = st.session_state["recurring_df"]
        if len(recurring_df) == 0:
            st.write("No dataframe available")
        else:
            filter_prompt = st.checkbox("Use filter")
            # condition if user want to use filter
            if filter_prompt is False:
                st.write(recurring_df)
            else:
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

                # only one filter is chosen
                if len(option) == 1:
                    if "Category" in option:
                        category = sf.filter_category()
                        mask_category = recurring_df["category"] == category
                        filtered_df = recurring_df[mask_category]

                    else:
                        importance = sf.filter_importance()
                        mask_importance = recurring_df["importance"] == importance
                        filtered_df = recurring_df[mask_importance]
                    # check if filtered_df exists
                    if len(filtered_df) != 0:
                        st.write(filtered_df)
                    else:
                        st.write("No data available")
                  
                if len(option) == 2:
                    col1, col2 = st.columns(2)
                    with col1:
                        category = sf.filter_category()
                    with col2:
                        importance = sf.filter_importance()
                    mask_category = recurring_df["category"] == category
                    mask_importance = recurring_df["importance"] == importance
                    filtered_df = recurring_df[mask_category & mask_importance]
                    # check if filtered_df exists
                    if len(filtered_df) != 0:
                        st.write(filtered_df)
                    else:
                        st.write("No data available")
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
            - if "item" and "amount" is not None, then proceed to next step
            - notify as invalid input,
            - if "item" is None
            - if "amount" is 0
        3. Store the new dataframe
            - if no dataframe available, create new one
            - if dataframe already exist, merge with new dataframe and save it
        4. Load it into session_state
    """
    recurring_df = enter_recurring()  # 1
    submit = st.button("Submit")
    if submit:
        if recurring_df["item"][0] != "" and recurring_df["amount"][0] != 0:  # 2
            recurring_df = store(recurring_df)  # 3
            st.session_state["recurring_df"] = recurring_df  # 4
            st.info("Saved successfully", icon="\U00002728")
        else:
            st.write("Invalid input")


if option == options[1]:
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
        recurring_df = st.session_state["recurring_df"]
        # 2
        delete_df = delete_recurring()
        # 3
        if delete_df is not None:
            submit = st.button("Delete")
            if submit:
                st.write("Deleted successfully")
                # 4
                recurring_df = recurring_df.drop(index=delete_df.index.values, axis=1)
                # 5
                recurring_df.to_csv(datasets_PATH, index=False)
                st.info("Your new dataframe!", icon="\U0001F680")
                if len(recurring_df) == 0:
                    st.write("No dataframe available")
                else:
                    st.write(recurring_df)  # new dataframe
                # save it again in session_state
                st.session_state["recurring_df"] = recurring_df
    else:
        st.write("No dataframe available")

if option == options[2]:
    view_recurring()
