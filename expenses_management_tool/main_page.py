import streamlit as st
import pandas as pd


# Sidebar setup
st.sidebar.markdown("Do you have a csv file?")
# Button to upload csv file
upload_file = st.sidebar.file_uploader("Upload your csv here")

# Check if file has been uploaded
if upload_file is not None:
    df = pd.read_csv(upload_file)
    st.session_state["df"] = df


st.title("Expenses")
# st.write("What are you spend?")


def enter_data():
    """
    Function to enter a single data entry
    """
    col1, col2 = st.columns(2)  # Create two container side by side

    with col1:
        name = st.text_input("Item")
        price = st.number_input("Price")
        category = st.selectbox(
            "Categories", ("Groceries", "Entertainment", "Transportation")
        )

    with col2:
        # st.write("Date")
        st.date_input("Date")
        st.slider("Importance scale", min_value=1, max_value=4)
        st.radio("How you are feeling on this purchase", ("Good", "Bad"))

    st.button("submit")


def delete_data():
    """
    Function to delete a single data entry from dataframe
    """
    pass


def edit_data():
    """
    Function to edit a column in dataframe
    """
    pass


def view_data():
    """
    Function to view the dataframe
    """
    if upload_file is not None:
        st.write(df)
    else:
        st.write("No dataframe available")


options = ["Enter single entry", "Delete entry", "Edit entry", "View your dataframe"]

# Create a select box
option = st.selectbox("What you want to do", options)

if option == options[0]:
    enter_data()

if option == options[1]:
    delete_data()

if option == options[2]:
    edit_data()

if option == options[3]:
    view_data()
