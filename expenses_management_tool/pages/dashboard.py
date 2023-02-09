import os
import streamlit as st
import plotly.express as px
import pandas as pd

# Get the right working directory
root = os.getcwd()
datasets = "datasets"
FILENAME = { "expenses" : "expenses_dataset.csv", "recurring" : "recurring_expenses.csv", "income" : "income_dataset.csv"}

months = {
"Jan" : 1,
"Feb" : 2,
"Mar" : 3,
"Apr" : 4,
"May" : 5,
"Jun" : 6,
"Jul" : 7,
"Aug" : 8,
"Sep" : 9,
"Oct" : 10,
"Nov" : 11,
"Dec" : 12}

st.title("Dashboard")

# Create the dropdown list
selected_file = st.sidebar.selectbox("Select your CSV file", FILENAME.keys())

for file in FILENAME.values():
    try:
        # Load the dataset
        datasets_PATH = os.path.join(root, datasets, file)
        st.session_state[file] = pd.read_csv(datasets_PATH)
    except:
        st.sidebar.write(f"No {file} file found")

if f"{FILENAME[selected_file]}" in st.session_state:
    
    inc_df = st.session_state["income_dataset.csv"]
    recex_df = st.session_state["recurring_expenses.csv"]
    ex_df = st.session_state["expenses_dataset.csv"]
    
    # select time span
    selected_month = st.sidebar.selectbox("Choose month", months.keys())
    selected_year = st.sidebar.selectbox("Choose year", ex_df["year"].unique().tolist()[::-1])
    
    def select_time_span():
        
        if selected_file == "recurring":
            filtered_df = st.session_state[FILENAME[selected_file]]
            st.write(filtered_df)
        else:
            mask = (st.session_state[FILENAME[selected_file]]["month"] == months[selected_month]) | (st.session_state[FILENAME[selected_file]]["month"].isna())
            filtered_df = st.session_state[FILENAME[selected_file]][mask]
            st.write(filtered_df)
            
    def Financial_overview():
        
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
    Financial_overview()
    select_time_span()
    
    #test
    st.write(months[selected_month])
    