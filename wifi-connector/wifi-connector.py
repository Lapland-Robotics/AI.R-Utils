from flask import Flask, request, jsonify
import subprocess
import re
import time

app = Flask(__name__)

predefined_wifi = {
}


@app.route('/scan', methods=['GET'])
def wifi_scan():
    # Command to scan available WiFi networks
    cmd = ['nmcli', 'device', 'wifi', 'list']
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        output = result.stdout
        # Extracting available WiFi networks
        networks = re.findall(r'\s+(.*?)\s+\d+\s+(.*?)\s+(.*?)\s+[\n\r]', output)
        available_networks = [{'SSID': net[0], 'BSSID': net[1], 'MODE': net[2]} for net in networks]
        
        return jsonify({'available_networks': available_networks}), 200
    else:
        return jsonify({'message': 'Failed to scan WiFi networks', 'error': result.stderr}), 500


@app.route('/connect', methods=['POST'])
def connect_wifi():
    data = request.json
    ssid = data.get('ssid')
    password = data.get('password')

    wifi_scan()
    time.sleep(20)

    cmd = ['nmcli', 'device', 'wifi', 'list']
    subprocess.run(cmd, capture_output=True, text=True)
    
    subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password])
    return jsonify({'message': f'Connected to {ssid}'})

@app.route('/status', methods=['GET'])
def get_status():
    # Command to get WiFi status
    cmd = ['nmcli', 'device', 'show']
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        output = result.stdout
        # Extracting current WiFi network name
        current_network_match = re.search(r'GENERAL\.CONNECTION: (.*?)[\n\r]', output)
        current_network = current_network_match.group(1).strip() if current_network_match else None

        # Extracting current IP address
        ip_match = re.search(r'IP4\.ADDRESS\[1\]:\s+(.*?)\/', output)
        ip_address = ip_match.group(1).strip() if ip_match else None

        return jsonify({'current_network': current_network, 'ip_address': ip_address}), 200
    else:
        return jsonify({'message': 'Failed to fetch WiFi status', 'error': result.stderr}), 500

def turn_on_wifi():
    # Check if WiFi is enabled
    cmd_check_wifi = ['nmcli', 'radio', 'wifi']
    result = subprocess.run(cmd_check_wifi, capture_output=True, text=True)
    
    if result.returncode == 0:
        if 'enabled' not in result.stdout.lower():  # WiFi is currently off
            # Turn on WiFi
            cmd_turn_on_wifi = ['nmcli', 'radio', 'wifi', 'on']
            subprocess.run(cmd_turn_on_wifi)
            time.sleep(20)
            print("WiFi turned on successfully.")
        else:
            print("WiFi is already turned on.")
    else:
        print("Failed to check WiFi status.")

if __name__ == '__main__':
    # Check predefined Wi-Fi networks and connect if available
    connected = False
    # turn on (conditional) the wifi
    turn_on_wifi()
    for ssid, password in predefined_wifi.items():
        try:
            subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password], check=True)
            connected = True
            break
        except subprocess.CalledProcessError:
            pass
    
    # Run Flask app binding to all network interfaces
    app.run(host='0.0.0.0', debug=True)
