import os
import streamlit as st
import plotly.express as px
import pandas as pd

# Get the right working directory
root = os.getcwd()
datasets = "datasets"
FILENAME = ["recurring_expenses.csv", "income_dataset.csv", "expenses_dataset.csv"]

st.title("Dashboard")

# Create the dropdown list
selected_file = st.sidebar.selectbox("Select your CSV file", FILENAME)

for file in FILENAME:
    try:
        # Load the dataset
        datasets_PATH = os.path.join(root, datasets, file)
        st.session_state[file] = pd.read_csv(datasets_PATH)
    except:
        st.sidebar.write(f"No {file} file found")

if f"{selected_file}" in st.session_state:
    inc_df = st.session_state["income_dataset.csv"]
    recex_df = st.session_state["recurring_expenses.csv"]
    ex_df = st.session_state["expenses_dataset.csv"]
    
    # Financial overview bar plot
    y1 = inc_df["amount"].sum()
    y2 = recex_df["amount"].sum() + ex_df["amount"].sum()
    
    df = pd.DataFrame({"Financial overview": [y2, y1], "Index": [2,1]})
    
    fig = px.bar(df, x="Financial overview", y="Index", 
                 color=["expenses", "income"], 
                 color_discrete_sequence=[px.colors.qualitative.Alphabet[1], px.colors.qualitative.Plotly[2]], 
                 orientation="h", 
                 barmode="stack")
    
    # Change size and width
    fig.update_layout(width=800, height=200)
    
    st.plotly_chart(fig)
    st.write(f"Total income : {y1}")
    st.write(f"Total expenses : {y2}")
    
    # Print selected DF
    st.write(st.session_state[f"{selected_file}"])
    
    
    