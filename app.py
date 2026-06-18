import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = '/tmp/data.json'

# ============================================================
# DATOS POR DEFECTO (con todos los jugadores actualizados)
# ============================================================
DEFAULT_DATA = {
    "ligaLogo": None,
    "teams": [
        # ------------------------------------------------------------
        # 1. Juventus Playa
        # ------------------------------------------------------------
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
        # ------------------------------------------------------------
        # 2. Spurs La Lisa FC
        # ------------------------------------------------------------
        {
            "id": 2,
            "name": "Spurs La Lisa FC",
            "logo": None,
            "players": [
                {"number": 1, "name": "Bartolo", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Richard", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Frank", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Cristofer", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Ronaldo", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Dariel", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Cristian", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Dayron", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Yoel", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 11, "name": "Sergio", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Yotuel", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 14, "name": "Zander", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 15, "name": "Aroko", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        # ------------------------------------------------------------
        # 3. Bastard München
        # ------------------------------------------------------------
        {
            "id": 3,
            "name": "Bastard München",
            "logo": None,
            "players": [
                {"number": 1, "name": "Jorgito", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Carlos", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Javier", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Eikon", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 12, "name": "Lionel", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "David", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Jean Carlos", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 11, "name": "Alex", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 15, "name": "Carlos", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 23, "name": "Maykol", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Bairon", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 18, "name": "Jorge", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 19, "name": "Jose Carlos", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        # ------------------------------------------------------------
        # 4. Galácticos FC
        # ------------------------------------------------------------
        {
            "id": 4,
            "name": "Galácticos FC",
            "logo": None,
            "players": [
                {"number": 1, "name": "Marlon", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Maikel", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Pedro", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Jose", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Carlos", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Rey", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Junior", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Luca", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Juan Carlos", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 11, "name": "William", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 14, "name": "Didier", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Diego", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 15, "name": "Anthony", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 16, "name": "David", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        # ------------------------------------------------------------
        # 5. Romanos FC (se mantienen los jugadores genéricos)
        # ------------------------------------------------------------
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
        # ------------------------------------------------------------
        # 6. FC Cubanacan
        # ------------------------------------------------------------
        {
            "id": 6,
            "name": "FC Cubanacan",
            "logo": None,
            "players": [
                {"number": 1, "name": "Jorge", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 13, "name": "Adrian", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Alex", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Raid", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Miguel", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Jorge", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Junior", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Daniel", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Darío", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Akon", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "José", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        # ------------------------------------------------------------
        # 7. Redbull FC
        # ------------------------------------------------------------
        {
            "id": 7,
            "name": "Redbull FC",
            "logo": None,
            "players": [
                {"number": 1, "name": "Diego", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Jose Angel", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Luis David", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Alain", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Sergio", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Thiago", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Holier", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Keiler", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Anthony", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Maykol", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 11, "name": "Esteben", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 14, "name": "Ernesto", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
            ],
            "fixtures": [],
            "friendlies": [],
            "wins": 0, "draws": 0, "losses": 0, "gf": 0, "gc": 0, "matches": 0, "points": 0, "gd": 0
        },
        # ------------------------------------------------------------
        # 8. Marsella FC
        # ------------------------------------------------------------
        {
            "id": 8,
            "name": "Marsella FC",
            "logo": None,
            "players": [
                {"number": 1, "name": "Piti", "position": "Portero", "goals": 0, "assists": 0, "img": None},
                {"number": 2, "name": "Marcel", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 3, "name": "Mauro", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 4, "name": "Lenier", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 5, "name": "Miguel Angel", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 6, "name": "Gordillo", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 7, "name": "Daniel", "position": "Defensa", "goals": 0, "assists": 0, "img": None},
                {"number": 8, "name": "Edian", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 9, "name": "Ever", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 10, "name": "Cucho", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 11, "name": "Andy", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 12, "name": "Jesus", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 13, "name": "Josiel", "position": "Centrocampista", "goals": 0, "assists": 0, "img": None},
                {"number": 14, "name": "Raiko", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 15, "name": "Pingora", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 16, "name": "Yosely", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 17, "name": "Ricurita", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 18, "name": "Julio", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 19, "name": "Tin Tin", "position": "Delantero", "goals": 0, "assists": 0, "img": None},
                {"number": 20, "name": "Coco", "position": "Delantero", "goals": 0, "assists": 0, "img": None}
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
