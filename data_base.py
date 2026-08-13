import sqlite3
import hashlib
import discord
from discord.ext import commands
from dotenv import load_dotenv

#!funciones hash
#*hash_generator....................................................................../

def machine_hash(path_file):
    with open (path_file, "rb") as file_rb:
        final_file = file_rb.read()
        hash_machine = hashlib.sha256()
        hash_machine.update(final_file)
        final_hash = hash_machine.hexdigest()
        return final_hash
#*.................................................................................../

#! funciones SQlite3
#*................................................................................../

def make_base():
    base = sqlite3.connect("scans.db") #creacion de base de datos
    cursor = base.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS base_bot(hash TEXT PRIMARY KEY, trigger TEXT, file_name TEXT)")
    base.commit()
    base.close()
#*..................................................................................

def id_table():
    id_table = sqlite3.connect("scans.db")  #creacion de tablas
    command_table = id_table.cursor()
    command_table.execute("CREATE TABLE IF NOT EXISTS server_bot(id_hash TEXT PRIMARY KEY, trigger_alerts TEXT)")
    id_table.commit()
    id_table.close()
#*................................................................................../

def save_result(hash_variable, result_variable, file_name_variable):
    save_result = sqlite3.connect("scans.db")
    command_save = save_result.cursor()
    command_save.execute("INSERT OR IGNORE INTO base_bot(hash, trigger, file_name) VALUES (?, ?, ?)", (hash_variable, result_variable, file_name_variable))
    save_result.commit()
    save_result.close()
#*................................................................................../

def lock_hash(hash_variable):
    lock_hash = sqlite3.connect("scans.db")
    command_lock = lock_hash.cursor()
    command_lock.execute("SELECT trigger FROM base_bot WHERE hash = ?", (hash_variable,))
    row = command_lock.fetchone()
    lock_hash.close()
    return row[0] if row else None
#*................................................................................../
 
def get_history():
    get_history = sqlite3.connect("scans.db") #historial de la tabla
    command_select = get_history.cursor()
    command_select.execute("SELECT file_name, trigger FROM base_bot LIMIT 10") #ultimos 10 cambios de la tabla "file_name" y "trigger"
    history_result = command_select.fetchall()  
    get_history.close() 
    return history_result 
#*................................................................................../
def cargar_css(ruta_archivo="styles.css"):
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True) #!funcion que invoca el estilo.css para el codigo fuente
#*prueba