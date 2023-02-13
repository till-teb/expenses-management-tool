import os
import streamlit as st
import plotly.express as px
import pandas as pd

# get the right working directory
root = os.getcwd()
datasets = "datasets"
FILENAME = { "expenses" : "expenses_dataset.csv", 
            "recurring" : "recurring_expenses.csv", 
            "income" : "income_dataset.csv"}

months = {"Jan" : 1,
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

# create the dropdown list
selected_file = st.sidebar.selectbox("Select your CSV file", FILENAME.keys())

for file in FILENAME.values():
    datasets_path = os.path.join(root, datasets, file)
    try:
        # Load the dataset
        st.session_state[file] = pd.read_csv(datasets_path)
    except:
        st.sidebar.write(f"No {file} file found")

# if file is found, select time span and finance mask
if FILENAME[selected_file] in st.session_state:
    
    selected_month = st.sidebar.selectbox("Choose month", months.keys())
    selected_year = st.sidebar.selectbox( "Choose year", st.session_state["expenses_dataset.csv"]["year"].unique().tolist())
    
    # create mask for month/year
    inc_mask = ((st.session_state["income_dataset.csv"]["month"] == months[selected_month])
                & (st.session_state["income_dataset.csv"]["year"] == selected_year)
                | (st.session_state["income_dataset.csv"]["month"].isna()))
    
    ex_mask = ((st.session_state["expenses_dataset.csv"]["month"] == months[selected_month])
               & (st.session_state["expenses_dataset.csv"]["year"] == selected_year)
               | (st.session_state["expenses_dataset.csv"]["month"].isna()))

    # apply mask
    inc_df = st.session_state["income_dataset.csv"][inc_mask]
    recex_df = st.session_state["recurring_expenses.csv"]
    ex_df = st.session_state["expenses_dataset.csv"][ex_mask]
    
    def Financial_overview():
        
        # financial overview bar plot
        y1 = inc_df["amount"].sum()
        y2 = recex_df["amount"].sum() + ex_df["amount"].sum()

        df = pd.DataFrame({"Financial overview": [y2, y1], "Index": [2,1]})

        fig = px.bar(df, x="Financial overview", y="Index", 
                 color=["expenses", "income"], 
                 color_discrete_sequence=[px.colors.qualitative.Alphabet[1], px.colors.qualitative.Plotly[2]], 
                 orientation="h", 
                 barmode="stack")
        

