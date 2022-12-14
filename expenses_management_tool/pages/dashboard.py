import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title("Dashboard")

if "df" not in st.session_state:
    st.write("Please upload your csv or enter your data to see your dashboard")


if "df" in st.session_state:
    df = st.session_state["df"]
    st.write(df)

    category = df["category"].value_counts()



    st.header("Spend by category")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        category,
        labels=(category.index),
        wedgeprops={"linewidth": 7, "edgecolor": "white"},
    )
    # display a white circle in the middle of the pie chart
    p = plt.gcf()
    p.gca().add_artist(plt.Circle((0, 0), 0.7, color="white"))
    st.pyplot(fig)


# Categories

    category = df["importance"].value_counts()
     
     
     
    st.header("distribution of importance")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        category,
        labels=(category.index),
        wedgeprops={"linewidth": 7, "edgecolor": "white"},
    )
    # display a white circle in the middle of the pie chart
    p = plt.gcf()
    p.gca().add_artist(plt.Circle((0, 0), 0.7, color="white"))
    st.pyplot(fig)
    
# amount plot

    st.header("amount range")
    barh_data = df["amount"]
    fig, ax = plt.subplots()
    ax.barh(barh_data,width=1)
    st.bar_chart(barh_data)

    

