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

        fig.update_layout(width=800, height=200)
        
        st.plotly_chart(fig)
        
        st.write(f"Total income {selected_month}. : ", y1)
        st.write(f"Total expenses {selected_month}. : ", y2)
        
    def pie_plot(filtered_df, selection, title, width=800, height=400):
        
        # group by category and sum the amounts
        category_group = filtered_df.groupby(selection)["amount"].sum().reset_index()
        fig = px.pie(category_group, values="amount", names=selection)
        
        # change size and width
        fig.update_layout(title=title, width=width, height=height)
        
        st.plotly_chart(fig)

    def credit_line_plot(width=800, height=400):
        
        # check for data
        if len(ex_df) != 0:
            # calculation of expenses on credit of the month
            sort_df_expenses = ex_df.sort_values(["day"], ascending=True)
            sort_df_expenses.iloc[0, sort_df_expenses.columns.get_loc("amount")] += recex_df["amount"].sum()
            sort_df_expenses["sum"] = sort_df_expenses["amount"].cumsum()
            
            # check if entry has na value on day
            na_inc_mask = inc_df["day"].isna()
            sort_df_expenses["inc_values"] = inc_df["amount"][na_inc_mask].sum()
    
            # check if entry has same value on day and add this to the total subsequent entries
            for index, row in sort_df_expenses.iterrows():
                day = row["day"]
                match = inc_df[inc_df["day"] == day]
                if not match.empty:
                    sort_df_expenses.at[index, "inc_values"] += match["amount"]   
            
            # calculates the total value amount
            sort_df_expenses["credit"] = sort_df_expenses["inc_values"] - sort_df_expenses["sum"]
            
            # plot
            fig = px.line(sort_df_expenses, x="day", y="credit", title=f"Credit history over the month {selected_month} :")
            
            fig.update_layout(width=width, height=height)
            st.plotly_chart(fig)
            st.write("Your current balance this month is : ", sort_df_expenses.iloc[-1, sort_df_expenses.columns.get_loc("credit")])
        
        #if there is no data
        else:
            st.info("No expenses available to display calculatation for this month", icon="\U0001F635")
            
    # importance over the month
    def importance_plot(width=400, height=400):
    
        # counts the number of occurring values in importance
        ex_df_imp = ex_df["importance"]
        recex_df_imp = recex_df["importance"]
        holder = pd.concat([ex_df_imp, recex_df_imp], axis=0)
        imp_counts = holder.value_counts()

        # plot
        fig = px.bar(imp_counts, x=imp_counts.index, y=imp_counts.values)
        fig.update_layout(title="Importance for the expenses :", xaxis_title="Importance", yaxis_title="Amount", width=width, height=height)

        st.plotly_chart(fig)
        
        st.write("Median importance of expenses this month : ", holder.median())
    
    # feeling over the month
    def feeling_plot(width=400, height=400):
    
        # counts the number of occurring values in feeling
        feeling_counts = ex_df["feeling"].value_counts()

        # plot
        fig = px.bar(feeling_counts, x=feeling_counts.index, y=feeling_counts.values)
        fig.update_layout(title="Feelings about the expenses :", xaxis_title="Feeling", yaxis_title="Amount", width=width, height=height)

        st.plotly_chart(fig)
        
        # print most frequent value
        most_frequent = ex_df["feeling"].value_counts().idxmax()
        st.write("Most common feeling this month : ", most_frequent)
    
    # MAIN:
    # all plots for the selected time period are loaded here
    Financial_overview()

    if selected_file == "recurring":
        filtered_df = st.session_state[FILENAME[selected_file]]
    else:
        mask = (st.session_state[FILENAME[selected_file]]["month"] == months[selected_month]) & (st.session_state[FILENAME[selected_file]]["year"] == selected_year) | (st.session_state[FILENAME[selected_file]]["month"].isna())
        filtered_df = st.session_state[FILENAME[selected_file]][mask]
    
    # creit plot
    credit_line_plot()
    
    st.subheader(f"{selected_file}:")
    
    # print daterframe from selected_file of the month
    st.write(filtered_df)
    st.write(f"The total amount of category {selected_file} is : ", filtered_df["amount"].sum())
    
    st.subheader("Details :")
    
    select_category = st.selectbox("Select details", ["Feeling details", "Categorie details"])
    
    if select_category == "Feeling details":
        
        # check for data
        if len(ex_df) != 0:
            col1, col2 = st.columns(2)
                  
            # first column content
            with col1:                  
                #feeling plot
                feeling_plot()
           
            # second column content
            with col2:
                # importence plot
                importance_plot()
        
        #if there is no data
        else:
            st.info("No expenses available to display calculatation for this month", icon="\U0001F635")
        
    else: 
        
        # to avoid conflict with non-existent column
        if selected_file == "income":
            
            pie_plot(filtered_df, "category", title="Categories")
        
        else:
            
            # select box category
            select_category = st.selectbox("Subcategory", filtered_df["category"].unique().tolist())
            
            # initiate 2 container side by side
            col1, col2 = st.columns(2)
            
            # first column content
            with col1:
                
                # call the pie plot function
                pie_plot(filtered_df, "category", title="Categories", width=400, height=400)
                
            # second column content
            with col2:
                
                # call the pie plot function with subcategory
                pie_plot(filtered_df[filtered_df["category"] == select_category], "subcategory", title="Subcategories", width=400, height=400)

