# Fichier: utils.py
import sqlite3
import pandas as pd
import streamlit as st
import json

DB_NAME = 'workout_data.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS routines (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, exercises TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, routine_name TEXT,
                 exercise_name TEXT, reps INTEGER, weight REAL)''')
    conn.commit()
    conn.close()

def get_routines():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql('SELECT * FROM routines', conn)
    conn.close()
    return df

def add_routine(name, exercises_list):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO routines (name, exercises) VALUES (?, ?)',
                  (name, json.dumps(exercises_list)))
        conn.commit()
        st.success(f"Routine '{name}' ajoutée !")
        return True
    except sqlite3.IntegrityError:
        st.error("Nom déjà pris.")
        return False
    finally:
        conn.close()

def update_routine(routine_id, original_name, new_name, new_exercises_list):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('UPDATE routines SET name = ?, exercises = ? WHERE id = ?',
                  (new_name, json.dumps(new_exercises_list), routine_id))
        if original_name != new_name:
            c.execute('UPDATE logs SET routine_name = ? WHERE routine_name = ?',
                      (new_name, original_name))
        conn.commit()
        st.success("Routine mise à jour !")
        return True
    except sqlite3.IntegrityError:
        st.error("Ce nom existe déjà.")
        return False
    finally:
        conn.close()

def delete_routine(routine_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM routines WHERE id = ?', (routine_id,))
    conn.commit()
    conn.close()

def save_log(date_val, routine, exercise, reps, weight):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO logs (date, routine_name, exercise_name, reps, weight) VALUES (?, ?, ?, ?, ?)',
              (date_val, routine, exercise, reps, weight))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql('SELECT id, date, routine_name, exercise_name, reps, weight FROM logs ORDER BY date DESC, id DESC', conn)
    conn.close()
    return df

def update_log_database(changes, id_mapping):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if changes['edited_rows']:
        for row_idx, modifications in changes['edited_rows'].items():
            try:
                position = int(row_idx)
                db_id = id_mapping[position]  # ✅ Récupérer l'id réel via le mapping

                for col, val in modifications.items():
                    if col in ['date', 'routine_name', 'exercise_name', 'reps', 'weight']:
                        if col == 'date':
                            val = str(val).split('T')[0]
                        c.execute(f"UPDATE logs SET {col} = ? WHERE id = ?", (val, db_id))
            except Exception as e:
                st.error(f"Erreur update : {e}")

    if changes['deleted_rows']:
        for row_idx in changes['deleted_rows']:
            try:
                position = int(row_idx)
                db_id = id_mapping[position]  # ✅ Même correction pour les suppressions
                c.execute("DELETE FROM logs WHERE id = ?", (db_id,))
            except Exception as e:
                st.error(f"Erreur delete : {e}")

    conn.commit()
    conn.close()
    st.success("✅ Données sauvegardées !")
    st.rerun()
