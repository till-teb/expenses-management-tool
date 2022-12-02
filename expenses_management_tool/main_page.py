import streamlit as st
import pandas as pd
# st.markdown("page 2")
st.sidebar.markdown("page 2")

st.title("Expenses")
st.write("What are you spend?")


if st.checkbox("Upload csv files"):
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        st.session_state["df"] = dataframe 

if st.checkbox("Enter single entry"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Item")
        price = st.number_input("Price")
        category = st.selectbox(
            "Categories", ("Groceries", "Entertainment", "Transportation")
        )
        # st.write(f"{category} is chosen")
    
    with col2:
        # st.write("Date")
        st.date_input("Date")
        st.slider("Importance scale", min_value=1, max_value=4)
        st.radio("How you are feeling on this purchase", ("Good", "Bad"))
    
    st.button("submit")
