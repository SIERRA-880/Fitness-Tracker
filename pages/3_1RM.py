import streamlit as st
import pandas as pd
import utils

st.set_page_config(page_title="1RM", page_icon="")

st.title("1 RM")

df = utils.get_logs()

if not df.empty:
    ex_filter = st.selectbox("Choose Exercice", df['exercise_name'].unique())

    chart_data = df[df['exercise_name'] == ex_filter].copy().sort_values('date')
    st.line_chart(chart_data, x='date', y='weight')
else:
    st.write("Aucune donnée disponible.")
