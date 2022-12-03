import os
import streamlit as st
import pandas as pd


def enter_data():
    """
    Function to enter a single data entry
    """
    # define the categories
    categories = [
        "Food",
        "Consumer Goods",
        "Transportation",
        "House utilities",
        "Leisure & Entertainment",
        "Insurance & Taxes",
        "Bank & Savings Investment",
        "Other & Extraordinary",
    ]

    col1, col2 = st.columns(2)  # Create two container side by side
    with col1:
        item = st.text_input("Item")
        amount = st.number_input("Price")
        category = st.selectbox("Categories", (item for item in categories))

    with col2:
        # st.write("Date")
        DATE = st.date_input("Date")
        importance = st.slider("Importance scale", min_value=1, max_value=4)
        feeling = st.radio("How you are feeling on this purchase", ("Good", "Bad"))

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
