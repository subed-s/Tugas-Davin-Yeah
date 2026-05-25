from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Konfigurasi MQTT yang sama dengan ESP32
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "proyek/esp32/led_kontrol_123"

# Inisialisasi MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@app.route('/')
def index():
    # Menampilkan file HTML
    return render_template('index.html')

@app.route('/api/led', methods=['POST'])
def control_led():
    # Menerima perintah dari HTML dan mengirimkannya ke ESP32 via MQTT
    data = request.json
    state = data.get('state')
    
    if state in ['ON', 'OFF']:
        mqtt_client.publish(MQTT_TOPIC, state)
        print(f"Perintah dikirim: {state}")
        return jsonify({"status": "success", "state": state})
        
    return jsonify({"status": "error", "message": "Perintah tidak valid"}), 400

if __name__ == '__main__':
    print("Server berjalan di http://127.0.0.1:5000")
    app.run(debug=True, port=5000)