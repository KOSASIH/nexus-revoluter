from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO
import json
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management
socketio = SocketIO(app)

# Sample data for demonstration
users = {}
iot_devices = []
tokenized_assets = []

class IoTDevice:
    def __init__(self, device_id, device_type, location):
        self.device_id = device_id
        self.device_type = device_type
        self.location = location
        self.data = {}

    def collect_data(self):
        """Simulate data collection from the IoT device."""
        if self.device_type in ['solar_panel', 'wind_turbine']:
            self.data = {
                "energy_produced": self.simulate_energy_production(),
                "timestamp": datetime.now().isoformat()
            }
        elif self.device_type == 'smart_meter':
            self.data = {
                "energy_consumed": self.simulate_energy_consumption(),
                "timestamp": datetime.now().isoformat()
            }
        return self.data

    def simulate_energy_production(self):
        """Simulate energy production based on device type."""
        return round(random.uniform(0.5, 5.0), 2)  # Simulated energy production in kWh

    def simulate_energy_consumption(self):
        """Simulate energy consumption for smart meters."""
        return round(random.uniform(0.1, 3.0), 2)  # Simulated energy consumption in kWh

class TokenizedAsset:
    def __init__(self, asset_id, asset_type, owner):
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.owner = owner
        self.tokenized_value = 0  # Value in tokens

    def tokenize_asset(self, value):
        """Tokenize the asset and set its value."""
        self.tokenized_value = value

# User Authentication
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password  # Simple user storage
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'], iot_devices=iot_devices, tokenized_assets=tokenized_assets)

@app.route('/api/iot_data', methods=['GET'])
def get_iot_data():
    """API endpoint to get IoT data."""
    data = {device.device_id: device.collect_data() for device in iot_devices}
    return jsonify(data)

@app.route('/api/tokenized_assets', methods=['GET'])
def get_tokenized_assets():
    """API endpoint to get tokenized assets."""
    return jsonify({asset.asset_id: {"owner": asset.owner, "value": asset.tokenized_value} for asset in tokenized_assets})

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Example usage
if __name__ == "__main__":
    # Sample IoT devices and tokenized assets
    iot_devices.append(IoTDevice("SolarPanel_001", "solar_panel", "Rooftop"))
    iot_devices.append(IoTDevice("WindTurbine_001", "wind_turbine", "Field"))
    tokenized_assets.append(TokenizedAsset("CarbonCredit_001", "carbon_credit", "Miner_001"))
    tokenized_assets.append(TokenizedAsset("RealEstate_001", "real_estate", "Investor_001"))

    socketio.run(app, debug=True)
