import streamlit as st
import pandas as pd
import utils

st.set_page_config(page_title="Volume Load", page_icon="🏋️")

st.title("Volume Load")

df = utils.get_logs()

if not df.empty:
    ex_filter = st.selectbox("Choose Exercise", df['exercise_name'].unique())

    df_filtered = df[df['exercise_name'] == ex_filter].copy()

    if 'reps' in df_filtered.columns and 'weight' in df_filtered.columns:
        df_filtered['volume_load'] = df_filtered['weight'] * df_filtered['reps']

        chart_data = df_filtered.groupby('date')['volume_load'].sum().reset_index()
        chart_data = chart_data.sort_values('date')

        st.line_chart(chart_data, x='date', y='volume_load')
    else:
        st.error("Les colonnes 'weight' ou 'reps' sont manquantes dans les données.")

else:
    st.write("No data.")
