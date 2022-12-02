import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# st.markdown("main dashboard")
st.sidebar.markdown("main dashboard")

st.title("Financial tracker")
st.write("this is our first streamlit yahoo!")
st.write("we could put summary of the monthly expense here")


# Sidebar setup
st.sidebar.title('Sidebar')
upload_file = st.sidebar.file_uploader('Upload a file containing earthquake data')

# Check if file has been uploaded
if upload_file is not None:
    df = pd.read_csv(upload_file)
    st.session_state['df'] = df

if "df" in st.session_state:
    df = st.session_state["df"]
    st.write(df)
    
    pol_par = df['Category'].value_counts()
    
    st.header("Spend by category")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(pol_par, labels=(pol_par.index + ' (' + pol_par.map(str)
    + ')'), wedgeprops = { 'linewidth' : 7, 'edgecolor' : 'white'
    })
    #display a white circle in the middle of the pie chart
    p = plt.gcf()
    p.gca().add_artist(plt.Circle( (0,0), 0.7, color='white'))
    st.pyplot(fig)