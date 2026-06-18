import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)  # Permite peticiones desde cualquier origen

# --- RUTA DE LA BASE DE DATOS (disco persistente en /data) ---
DATA_DIR = os.environ.get('DATA_DIR', './data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'data.db')
print(f"📁 Usando base de datos en: {DB_PATH}")

# --- INICIALIZAR BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS app_data (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    # Si no hay datos, insertar estructura por defecto
    c.execute('SELECT value FROM app_data WHERE key = "ligaData"')
    if not c.fetchone():
        default_data = {
            "teams": [],
            "news": {"matches": [], "transfers": []}
        }
        c.execute('REPLACE INTO app_data (key, value) VALUES (?, ?)',
                  ("ligaData", json.dumps(default_data)))
        conn.commit()
    conn.close()

# --- RUTAS API ---
@app.route('/api/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT value FROM app_data WHERE key = "ligaData"')
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify(json.loads(row[0]))
    return jsonify({"teams": [], "news": {"matches": [], "transfers": []}})

@app.route('/api/data', methods=['POST'])
def save_data():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('REPLACE INTO app_data (key, value) VALUES (?, ?)',
              ("ligaData", json.dumps(data)))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

# --- ARRANQUE ---
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)