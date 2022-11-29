import streamlit as st

# st.markdown("page 2")
st.sidebar.markdown("page 2")

st.write("page to make input for expenses maybe?")
st.write("What are you spend?")

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

    # with col3:
    # st.write("Day label")
    st.radio("How you are feeling on this day", ("Good", "Bad"))

st.button("submit")
