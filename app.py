from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from threading import Thread
import time
import json
import random  # Fügen Sie diesen Import hinzu
import os
from config import AVAILABLE_APIS
from utils.custom_api import generate_asset, generate_assets, ASSET_TYPES

# Definieren Sie ASSET_TYPES hier, falls der Import immer noch nicht funktioniert
ASSET_TYPES = {
    "Information": "Information Asset",
    "Physical Assets": "Physical Asset",
    "Software": "Software Asset",
    "Services": "Service Asset",
    "Networks and Communications": "Network Asset",
    "Human Resources": "Human Resource Asset",
    "Financial Resources": "Financial Asset",
    "Reputation": "Reputation Asset",
    "Documented Procedures": "Procedure Asset"
}

app = Flask(__name__)
CORS(app)  # Dies erlaubt CORS für alle Routen
app.config['SECRET_KEY'] = 'ein_sehr_sicherer_und_zufälliger_schlüssel'  # Ändern Sie dies zu einem sicheren Wert
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)

CONFIG_FILE = 'current_config.json'

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

# Background task to simulate asset generation with logging
def generate_assets_with_logging(count, resource_selection, specific_types=None):
    if resource_selection == 'all':
        for i in range(1, count + 1):
            time.sleep(1)  # Simulate the time to generate an asset
            message = f"Generating asset {i} of {count} for all types"
            socketio.emit('log_message', {'message': message})
    else:
        for asset_type in specific_types:
            time.sleep(1)  # Simulate the time to generate a specific asset
            message = f"Generating asset for type {asset_type}"
            socketio.emit('log_message', {'message': message})
    socketio.emit('log_message', {'message': 'Asset generation completed.'})

@app.route('/')
def index():
    return render_template('index.html', available_apis=AVAILABLE_APIS.keys(), asset_types=ASSET_TYPES.keys())

@app.route('/generate_assets', methods=['POST'])
def generate_assets_route():
    api = request.form.get('api')
    auth_type = request.form.get('auth_type')
    credentials = request.form.get('credentials')
    resource_selection = request.form.get('resource_selection')
    all_types_count = int(request.form.get('all_types_count', 10))
    specific_types = request.form.getlist('resource_types')
    
    if resource_selection == 'specific':
        specific_type_counts = json.loads(request.form.get('specific_type_counts', '{}'))
    else:
        specific_type_counts = {}

    config = {
        "api": api,
        "auth_type": auth_type,
        "credentials": credentials,
        "resource_selection": resource_selection,
        "all_types_count": all_types_count,
        "specific_types": specific_types,
        "specific_type_counts": specific_type_counts
    }

    save_config(config)
    print(f"Debug - Saved Config: {config}")  # Debug output

    # Generate a sample set of assets to return the count
    sample_assets = []
    if resource_selection == 'all':
        sample_assets = generate_assets(all_types_count)
    else:
        for asset_type in specific_types:
            count = int(specific_type_counts.get(asset_type + "_count", 10))
            sample_assets.extend(generate_assets(count, asset_type))

    sample_assets = sample_assets[:all_types_count]

    return jsonify({"config": config, "assets_count": len(sample_assets)})

@app.route('/get_generated_assets', methods=['GET'])
def get_generated_assets():
    assets = session.get('generated_assets', [])
    return jsonify(assets)

@app.route('/get_api_url', methods=['POST'])
def get_api_url():
    api = request.json.get('api')
    url = AVAILABLE_APIS.get(api, "URL not available")
    return jsonify({"url": url})

@app.route('/custom_api/v1', methods=['GET'])
def custom_api():
    config = load_config()
    
    print(f"Debug - Retrieved Config: {config}")  # Debug output

    # Generate new assets based on the config
    all_types_count = config.get('all_types_count', 10)
    resource_selection = config.get('resource_selection', 'all')
    specific_types = config.get('specific_types', [])
    specific_type_counts = config.get('specific_type_counts', {})

    assets = []
    if resource_selection == 'all':
        assets = generate_assets(all_types_count)
    else:
        for asset_type in specific_types:
            count = int(specific_type_counts.get(asset_type + "_count", 10))
            assets.extend(generate_assets(count, asset_type))

    assets = assets[:all_types_count]

    print(f"Debug - Generated Assets Count: {len(assets)}")  # Debug output

    return jsonify(assets)

@app.route('/check_config', methods=['GET'])
def check_config():
    return jsonify(load_config())

@app.route('/clear_config', methods=['GET'])
def clear_config():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    return jsonify({"message": "Configuration cleared"})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
