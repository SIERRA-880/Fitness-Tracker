import streamlit as st
import pandas as pd
import numpy as np
import utils

st.set_page_config(page_title="ACWR", page_icon="🏋️")

st.title("Acute:Chronic Workload Ratio")

df = utils.get_logs()

if not df.empty:
    ex_filter = st.selectbox("Choose Exercise", df['exercise_name'].unique())

    df_filtered = df[df['exercise_name'] == ex_filter].copy()

    if 'reps' in df_filtered.columns and 'weight' in df_filtered.columns:
        df_filtered['volume_load'] = df_filtered['weight'] * df_filtered['reps']

        daily_vol = df_filtered.groupby('date')['volume_load'].sum()

        daily_vol.index = pd.to_datetime(daily_vol.index)
        daily_vol = daily_vol.asfreq('D', fill_value=0)

        acute_load = daily_vol.rolling(window=7, min_periods=1).mean()
        chronic_load = daily_vol.rolling(window=28, min_periods=1).mean()

        acwr = acute_load / chronic_load.replace(0, np.nan)

        if not acwr.dropna().empty:
            current_acwr = acwr.dropna().iloc[-1]

            if 0.8 <= current_acwr <= 1.3:
                state_msg = "Optimal Zone"
            elif current_acwr > 1.2:
                state_msg = "Risk"
            else:
                state_msg = "Detraining"

            col1, col2 = st.columns(2)
            col1.metric("Current ACWR", f"{current_acwr:.2f}", state_msg)
            col2.write("Sweet spot: **0.8 — 1.3**")

            st.line_chart(acwr.dropna())

        else:
            st.warning("Not enough data history to calculate ACWR (Need at least a few days).")

    else:
        st.error("Columns 'weight' or 'reps' are missing.")

else:
    st.write("No data.")
