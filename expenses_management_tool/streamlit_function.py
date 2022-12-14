import streamlit as st
import pandas as pd

# define the categories
categories = [
    "Consumables",
    "Food & Beverages",
    "Leisure & Entertainment",
    "Transportation",
    "Other & Extraordinary",
    "financial fees",
    "living area"
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
    ["taxes", "insurance", "bank"],
    ["energy", "rent","Household appliances ","decoration"]
]


def enter_data():
    """
    Function to add a single data entry
    ...
    return a new dataframe
    """
    col1, col2, col3 = st.columns(3)  # Initiate 3 columns
    # first column content
    with col1:
        item = st.text_input("Item")
        amount = st.number_input("Price")
        importance = st.slider("Importance scale", min_value=1, max_value=4)

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
    # third column content
    with col3:
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
    Function to filter category, useful for edit/delete data from dataframe
    ...
    return category from list of categories
    """
    option = st.selectbox("Choose category", (item for item in categories))
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

    elif "Month" in option:
        month = filter_month()  # get the entry from selected month
        mask = df["month"] == month
        filtered_df = df[mask]
        if len(filtered_df) == 0:
            st.write("No data available")
        else:
            st.write(filtered_df)

    elif "Category" in option:
        category = filter_category()  # get the entry from selected category
        mask = df["category"] == category
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
                st.write("No dataframe available")
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


def view_data():
    """
    Function to view the dataframe
    """
    # load the dataframe if it's available
    if "df" in st.session_state:
        df = st.session_state["df"]
        if len(df) == 0:
            st.write("No dataframe available")
        else:
            st.write(df)
    else:
        st.write("No dataframe available")
