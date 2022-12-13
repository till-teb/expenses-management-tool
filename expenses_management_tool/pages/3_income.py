import streamlit as st
import pandas as pd

st.title("Income")
st.subheader("Please enter all your income here")

options = ["Enter fixed income", "Enter additional income"]
categories = ["Salary", "Allowance", "Bonus", "Other"]

option = st.selectbox("What you want to do", options)

if option == options[0]:
    fixed_income = st.number_input("Your fixed income")
    category = st.selectbox("Category", (item for item in categories))

elif option == options[1]:
    additional_income = st.number_input(("Additional income"))
    category = st.selectbox("Category", (item for item in categories))
    
if "Other" in category:
    notes = st.text_input("Notes")