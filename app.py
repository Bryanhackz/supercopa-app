import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ruta del archivo JSON (usamos /tmp que siempre es escribible en Render)
DATA_FILE = '/tmp/data.json'

def load_data():
    """Carga los datos desde el archivo JSON. Si no existe, crea la estructura por defecto."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    # Datos por defecto (vacíos, el frontend los llenará)
    default = {"teams": [], "news": {"matches": [], "transfers": []}}
    save_data(default)
    return default

def save_data(data):
    """Guarda los datos en el archivo JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        data = load_data()
        return jsonify(data)
    except Exception as e:
        print(f"❌ Error en GET /api/data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/data', methods=['POST'])
def save_data_endpoint():
    try:
        data = request.json
        if data is None or not isinstance(data, dict):
            return jsonify({"error": "Datos inválidos"}), 400
        save_data(data)
        return jsonify({"ok": True})
    except Exception as e:
        print(f"❌ Error en POST /api/data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
