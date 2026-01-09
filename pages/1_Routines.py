import streamlit as st
import json
import utils

st.set_page_config(page_title="Routines Management", page_icon="")

st.title("Routines Management")
routines_df = utils.get_routines()

mode = st.radio("Action :", ["Create", "Edit"], horizontal=True)
st.divider()

if mode == "Create":
    st.subheader("Create a Routine")
    with st.form("add_r"):
        n = st.text_input("Routine Name")
        e = st.text_area("Exercices list (one by line)", height=150)
        if st.form_submit_button("Create routine"):
            if n and e:
                ex_list = [x.strip() for x in e.split('\n') if x.strip()]
                if utils.add_routine(n, ex_list): st.rerun()
            else:
                st.error("Le nom et les exercices sont obligatoires.")
else:
    st.subheader("Edit a Routine")
    if not routines_df.empty:
        r_edit = st.selectbox("Select a Routine", routines_df['name'].unique())
        curr = routines_df[routines_df['name'] == r_edit].iloc[0]
        curr_ex = "\n".join(json.loads(curr['exercises']))

        with st.form("edit_r"):
            nn = st.text_input("Name", value=r_edit)
            ne = st.text_area("Exercices", value=curr_ex, height=150)

            if st.form_submit_button("Save changes"):
                ex_list = [x.strip() for x in ne.split('\n') if x.strip()]
                if utils.update_routine(int(curr['id']), r_edit, nn, ex_list): st.rerun()

        st.write("")
        if st.button(f"Delete routine '{r_edit}'", type="primary"):
            utils.delete_routine(int(curr['id']))
            st.rerun()
    else:
        st.info("Aucune routine à modifier.")
