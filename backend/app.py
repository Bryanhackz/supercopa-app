import os
import sqlite3
import json
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite CORS para todas las rutas

# Configuración de la base de datos
DATA_DIR = os.environ.get('DATA_DIR', './data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'data.db')
print(f"📁 Usando base de datos en: {DB_PATH}")

def init_db():
    """Crea la tabla y los datos iniciales si no existen."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS app_data (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        # Verificar si existe la clave 'ligaData'
        c.execute('SELECT value FROM app_data WHERE key = "ligaData"')
        if not c.fetchone():
            # Datos iniciales con estructura básica
            default_data = {
                "teams": [],
                "news": {"matches": [], "transfers": []}
            }
            c.execute('REPLACE INTO app_data (key, value) VALUES (?, ?)',
                      ("ligaData", json.dumps(default_data)))
            conn.commit()
            print("✅ Base de datos inicializada con datos por defecto.")
        else:
            print("✅ Base de datos ya existente.")
        conn.close()
    except Exception as e:
        print("❌ Error en init_db:")
        traceback.print_exc()
        # No lanzamos excepción para que la app siga arrancando, pero luego fallarán las consultas

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT value FROM app_data WHERE key = "ligaData"')
        row = c.fetchone()
        conn.close()
        if row:
            try:
                data = json.loads(row[0])
                return jsonify(data)
            except json.JSONDecodeError:
                # Si el JSON está corrupto, devolvemos estructura vacía
                return jsonify({"teams": [], "news": {"matches": [], "transfers": []}})
        else:
            # Si no hay registro, devolvemos vacío
            return jsonify({"teams": [], "news": {"matches": [], "transfers": []}})
    except Exception as e:
        print("❌ Error en GET /api/data:")
        traceback.print_exc()
        # Devolvemos un error 500 con detalles (para depuración)
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route('/api/data', methods=['POST'])
def save_data():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "No se recibió JSON"}), 400
        # Validar estructura básica
        if not isinstance(data, dict) or "teams" not in data or "news" not in data:
            return jsonify({"error": "Estructura de datos inválida"}), 400

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('REPLACE INTO app_data (key, value) VALUES (?, ?)',
                  ("ligaData", json.dumps(data)))
        conn.commit()
        conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        print("❌ Error en POST /api/data:")
        traceback.print_exc()
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de salud para verificar que el servicio está funcionando."""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
