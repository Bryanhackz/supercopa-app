import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = '/tmp/data.json'

# ============================================================
# DATOS POR DEFECTO (con ligaLogo)
# ============================================================
DEFAULT_DATA = {
    "ligaLogo": None,
    "teams": [
        {
            "id": 1,
            "name": "Juventus Playa",
            "logo": None,
            "players": [
                {"number": 30, "name": "Dario", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 1, "name": "Samuel", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Daniel", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Raul", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 19, "name": "Dayan", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 17, "name": "Muñoz", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 50, "name": "Roldan", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 21, "name": "Rafael", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Alain", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 80, "name": "Frank", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 11, "name": "Miguel", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Diego", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 15, "name": "Dario", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Xavier", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 81, "name": "Henry", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Camilo", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Brayan", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [{"opponent": "Bastard München", "result": "5-2", "type": "Liga", "date": "2025-06-01"}],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        {
            "id": 2,
            "name": "Spurs La Lisa FC",
            "logo": None,
            "players": [
                {"number": 1, "name": "Portero1", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Defensa1", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Defensa2", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Defensa3", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Centro1", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Centro2", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Centro3", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Delantero1", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Delantero2", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Delantero3", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        {
            "id": 3,
            "name": "Bastard München",
            "logo": None,
            "players": [
                {"number": 1, "name": "Portero1", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Defensa1", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Defensa2", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Defensa3", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Centro1", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Centro2", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Centro3", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Delantero1", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Delantero2", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Delantero3", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        {
            "id": 4,
            "name": "Galácticos FC",
            "logo": None,
            "players": [
                {"number": 1, "name": "Portero1", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Defensa1", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Defensa2", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Defensa3", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Centro1", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Centro2", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Centro3", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Delantero1", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Delantero2", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Delantero3", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        {
            "id": 5,
            "name": "Romanos FC",
            "logo": None,
            "players": [
                {"number": 1, "name": "Portero1", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Defensa1", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Defensa2", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Defensa3", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Centro1", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Centro2", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Centro3", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Delantero1", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Delantero2", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Delantero3", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        {
            "id": 6,
            "name": "FC Cubanacan",
            "logo": None,
            "players": [
                {"number": 1, "name": "Portero1", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Defensa1", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Defensa2", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Defensa3", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Centro1", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Centro2", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Centro3", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Delantero1", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Delantero2", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Delantero3", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        {
            "id": 7,
            "name": "Redbull FC",
            "logo": None,
            "players": [
                {"number": 1, "name": "Portero1", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Defensa1", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Defensa2", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Defensa3", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Centro1", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Centro2", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Centro3", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Delantero1", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Delantero2", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Delantero3", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        {
            "id": 8,
            "name": "Marsella FC",
            "logo": None,
            "players": [
                {"number": 1, "name": "Portero1", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Defensa1", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Defensa2", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Defensa3", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Centro1", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Centro2", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Centro3", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Delantero1", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Delantero2", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Delantero3", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        }
    ],
    "news": {"matches": [], "transfers": []}
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data and isinstance(data, dict) and "teams" in data:
                    if "ligaLogo" not in data:
                        data["ligaLogo"] = None
                    return data
        except (json.JSONDecodeError, IOError):
            pass
    save_data(DEFAULT_DATA)
    return DEFAULT_DATA

def save_data(data):
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
