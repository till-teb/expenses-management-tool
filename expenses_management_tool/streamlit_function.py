import streamlit as st
import pandas as pd
import os

# get the right working directory
root = os.getcwd()
datasets = "datasets"
def load_datasets(FILENAME, df):
    try:
        # load the dataset, if it's available
        datasets_PATH = os.path.join(root, datasets, FILENAME)
        st.session_state[df] = pd.read_csv(datasets_PATH)
    except:
        st.sidebar.write("No csv file found")

# define the categories
categories = [
    "Consumables",
    "Food & Beverages",
    "Leisure & Entertainment",
    "Transportation",
    "Other & Extraordinary",
    "Financial fees",
    "Living area"
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
    ["Energy", "Rent", "Household Appliances ", "Decoration", "Other"]
]


def enter_data():
    """
    Function to add a single data entry
    ...
    return a new dataframe
    """
    col1, col2 = st.columns(2)  # Initiate 2 columns
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
        # show subcategory related to its main category
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

        DATE = st.date_input("Date")
        feeling = st.radio("How you are feeling on this day", ("Good", "Bad"))

    # save into a dataframe
    df = pd.DataFrame(
        {
            "item": [item],
            "amount": [amount],
            "category": [category],
            "subcategory": [subcategory],
            "importance": [importance],
            "DATE": [str(DATE)],
            "feeling": [feeling],
        }
    )
    return df


def filter_month():
    """
    Function to filter month, useful for edit/delete data from dataframe
    ...
    return a month number
    """
    months = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }

    month = st.selectbox("Choose month", (item for item in months.values()))

    for key, item in months.items():
        if item == month:
            month_num = key

    return month_num


def filter_category():
    """
    Function to filter category, useful for view/delete data from dataframe
    ...
    return category from list of categories
    """
    option = st.selectbox("Choose category", (item for item in categories))
    return option


def filter_importance():
    """
    Function to filter importance, useful for view/delete data from dataframe
    ...
    return importance from list of importances
    """
    option = st.selectbox("Choose importance", (_ for _ in range(1, 4)))
    return option


def delete_data():
    """
    Function to delete a single data entry from dataframe
    ...
    return a dataframe that should be deleted
    """
    # load the dataframe, if it's available
    if "df" in st.session_state:
        df = st.session_state["df"]
    else:
        st.write("No dataframe available")

    st.write("Do you wish to delete any data?")

    options = ["Month", "Category"]
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
        col1, col2 = st.columns(2)  # initiate 2 columns
        # first column content
        with col1:
            month = filter_month()
        # second column content
        with col2:
            category = filter_category()
        mask_month = df["month"] == month
        mask_category = df["category"] == category
        filtered_df = df[mask_month & mask_category]
        if len(filtered_df) == 0:
            st.write("No data available")
        else:
            st.write(filtered_df)

    elif len(option) == 1:
        if "Month" in option:
            month = filter_month()  # get the entry from selected month
            mask = df["month"] == month
            filtered_df = df[mask]

        if "Category" in option:
            category = filter_category()  # get the entry from selected category
            mask = df["category"] == category
            filtered_df = df[mask]

        # check if filtered_df exists
        if len(filtered_df) == 0:
            st.write("No data available")
        else:
            st.write(filtered_df)

    # if no filter is chosen
    elif len(option) == 0:
        filtered_df = df  # return df without filter
        st.write("No filter is chosen")
        st.write(filtered_df)
    
    if len(filtered_df) != 0:
        delete_index = st.multiselect(
            "Choose index to delete", (filtered_df.index.values)
        )
        delete_df = filtered_df.loc[delete_index]
        st.write("This entry will be deleted")
        if len(delete_df) == 0:
            st.write("No dataframe available")
        else:
            st.write(delete_df)
        return delete_df


def view_data():
    """
    Function to view the dataframe
    Has 3 filters which is category, month and importance
    ...
    return expenses dataframe
    """
    # load the dataframe if it's available
    if "df" in st.session_state:
        df = st.session_state["df"]
        if len(df) == 0:
            st.write("No dataframe available")
        else:
            filter_prompt = st.checkbox("Use filter")
            # condition if user want to use filter
            if filter_prompt is False:
                st.write(df)

            else:
                options = ["Month", "Category", "Importance"]
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
                    if "Month" in option:
                        month = filter_month()
                        mask_month = df["month"] == month
                        filtered_df = df[mask_month]
    
                    elif "Category" in option:
                        category = filter_category()
                        mask_category = df["category"] == category
                        filtered_df = df[mask_category]
    
                    else:
                        importance = filter_importance()
                        mask_importance = df["importance"] == importance
                        filtered_df = df[mask_importance]
    
                    # check if filtered_df exists
                    if len(filtered_df) != 0:
                        st.write(filtered_df)
                    else:
                        st.write("No data available")

                # only two filter are chosen
                elif len(option) == 2:
                    col1, col2 = st.columns(2)
                    if "Month" and "Category" in option:
                        with col1: 
                            month = filter_month()
                        with col2:
                            category = filter_category()
                        mask_month = df["month"] == month
                        mask_category = df["category"] == category
                        filtered_df = df[mask_month & mask_category]
    
                    elif "Importance" and "Category" in option:
                        with col1:
                            category = filter_category()
                        with col2:
                            importance = filter_importance()
                        mask_category = df["category"] == category
                        mask_importance = df["importance"] == importance
                        filtered_df = df[mask_category & mask_importance]
    
                    elif "Importance" and "Month" in option:
                        with col1:
                            month = filter_month()
                        with col2:
                            importance = filter_importance()
                        mask_month = df["month"] == month
                        mask_importance = df["importance"] == importance
                        filtered_df = df[mask_importance & mask_month]
                    
                    # check if filtered_df exists
                    if len(filtered_df) != 0:
                        st.write(filtered_df)
                    else:
                        st.write("No data available")

                # all filter are chosen
                elif len(option) == 3:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        month = filter_month()
                    with col2:
                        category = filter_category()
                    with col3:
                        importance = filter_importance()
                    
                    mask_month = df["month"] == month
                    mask_category = df["category"] == category
                    mask_importance = df["importance"] == importance
                    filtered_df = df[mask_month & mask_category & mask_importance]
                    if len(filtered_df) == 0:
                        st.write("No data available")
                    else:
                        st.write(filtered_df)
    else:
        st.write("No dataframe available")
