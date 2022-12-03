import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title("Dashboard")


if "df" in st.session_state:
    df = st.session_state["df"]
    st.write(df)

    pol_par = df["Category"].value_counts()

    st.header("Spend by category")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        pol_par,
        labels=(pol_par.index),
        wedgeprops={"linewidth": 7, "edgecolor": "white"},
    )
    # display a white circle in the middle of the pie chart
    p = plt.gcf()
    p.gca().add_artist(plt.Circle((0, 0), 0.7, color="white"))
    st.pyplot(fig)
