import streamlit as st
import pandas as pd
from datetime import date
import json
import utils

st.set_page_config(page_title="Workout Tracker", page_icon="")

# Initialisation DB au lancement
utils.init_db()

st.title("Today's Workout")

routines_df = utils.get_routines()

# --- DÉFINITION DU MODAL ---
@st.dialog("Add Exercice")
def show_entry_modal():
    # 1. Sélection de la date et de la Routine
    d = date.today()

    # On récupère la liste des routines
    r_name = st.selectbox("Routine", routines_df['name'].unique())

    # 2. Récupération dynamique des exercices liés à la routine choisie
    r_row = routines_df[routines_df['name'] == r_name].iloc[0]
    exs = json.loads(r_row['exercises'])
    ex = st.selectbox("Exercice", exs)

    # st.divider()

    # 3. Formulaire de saisie pour les chiffres
    with st.form("log_modal"):
        c1, c2 = st.columns(2)
        reps = c1.number_input("Reps", 1, value=10)
        w = c2.number_input("Poids (kg)", 0.0, step=0.5)

        # Bouton de soumission
        if st.form_submit_button("Add", use_container_width=True):
            utils.save_log(d, r_name, ex, reps, w)
            st.toast(f"Added : {ex} ({w}kg x {reps})")
            st.rerun()

# --- INTERFACE PRINCIPALE ---

if routines_df.empty:
    st.warning("⚠️ Aucune routine trouvée. Va dans le menu 'Gestion Routines' à gauche pour en créer une.")
else:
    # Bouton pour ouvrir le modal (remplace l'affichage direct des colonnes)
    if st.button("Add exercice", type="primary"):
        show_entry_modal()

    st.divider()

    # Affichage du tableau (inchangé)
    df_log = utils.get_logs()
    # On utilise un date_input ici aussi pour filtrer le tableau si besoin,
    # sinon on filtre sur la date d'aujourd'hui par défaut
    filter_date = date.today()

    if not df_log.empty:
        df_log['date_dt'] = pd.to_datetime(df_log['date']).dt.date
        todays = df_log[df_log['date_dt'] == filter_date]

        if not todays.empty:
            st.dataframe(
                todays[['exercise_name', 'weight', 'reps']],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(f"Rien d'enregistré pour le {filter_date}.")
    else:
        st.info("Aucun historique disponible.")
