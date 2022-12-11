import os
import streamlit as st
import pandas as pd

# define the categories
categories = [
    "Food",
    "Consumer Goods",
    "Transportation",
    "House utilities",
    "Leisure & Entertainment",
    "Insurance & Taxes", # fixed expenses
    "Bank & Savings Investment",
    "Other & Extraordinary",
]

subcategories = [["Bakery", "Kiosk", "Supermarket"], ["A", "B", "C"]]


def enter_data():
    """
    Function to enter a single data entry
    """
    col1, col2, col3 = st.columns(3)  # Create two container side by side
    with col1:
        item = st.text_input("Item")
        amount = st.number_input("Price")
        importance = st.slider("Importance scale", min_value=1, max_value=4)
   
    with col2:
        category = st.selectbox("Categories", (item for item in categories))
        
        if category == "Food":
            subcategory = st.selectbox("Subcategories", (item for item in subcategories[0]))
            
        elif category == categories[1]:
            subcategory = st.selectbox("Subcategories", (item for item in subcategories[1]))
              
    with col3:
        DATE = st.date_input("Date")
        feeling = st.radio("How you are feeling on this day", ("Good", "Bad"))
          
    df = pd.DataFrame(
        {
            "item": [item],
            "amount": [amount],
            "category": [category],
            "importance": [importance],
            "DATE": [str(DATE)],
            "feeling": [feeling],
        }
    )
    return df


def delete_data():
    """
    Function to delete a single data entry from dataframe
    """
    st.write("Do you wish to delete any data?")

    options = ["Month", "Category"]
    option = st.multiselect("Filter by", options)

    def filter_month():
        month = st.selectbox(
            "Choose month",
            (
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ),
        )

    pass  # will continue later


def edit_data():
    """
    Function to edit a column in dataframe
    """
    pass


def view_data():
    """
    Function to view the dataframe
    """
    if "df" in st.session_state:
        df = st.session_state["df"]
        st.write(df)
    else:
        st.write("No dataframe available")
