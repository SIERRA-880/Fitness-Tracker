import streamlit as st
import pandas as pd
import utils

st.set_page_config(page_title="History", page_icon="🏋️")

st.title("History")

df = utils.get_logs()

if not df.empty:
    df['date'] = pd.to_datetime(df['date'])

    # ✅ Garder le mapping position -> id AVANT de modifier le DataFrame
    id_mapping = df['id'].tolist()

    df = df.set_index('id')

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        key="history_editor",
        use_container_width=True,
        column_config={
            "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "weight": st.column_config.NumberColumn("Poids", format="%.1f kg"),
            "reps": "Reps",
            "exercise_name": "Exercice"
        }
    )

    if st.button("Save"):
        # ✅ Passer le mapping à la fonction
        utils.update_log_database(st.session_state["history_editor"], id_mapping)
else:
    st.write("No data.")
