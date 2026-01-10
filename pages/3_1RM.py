import streamlit as st
import pandas as pd
import utils

st.set_page_config(page_title="1RM", page_icon="🏋️")

st.title("1 RM Progress")

df = utils.get_logs()

if not df.empty:
    ex_filter = st.selectbox("Choose Exercise", df['exercise_name'].unique())

    df_filtered = df[df['exercise_name'] == ex_filter].copy()

    df_filtered['estimated_1rm'] = df_filtered['weight'] * (1 + df_filtered['reps'] / 30)

    best_1rm = df_filtered['estimated_1rm'].max()
    best_weight = df_filtered['weight'].max()

    col1, col2 = st.columns(2)
    col1.metric("1RM (Theorical)", f"{best_1rm:.1f} kg")
    col2.metric("PR", f"{best_weight} kg")

    chart_data = df_filtered.groupby('date')['weight'].max().reset_index()
    chart_data = chart_data.sort_values('date')

    st.line_chart(chart_data, x='date', y='weight')

else:
    st.write("No data.")
