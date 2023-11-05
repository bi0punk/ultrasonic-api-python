from flask import Flask, request, render_template, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

sensor_data = []  # Lista para almacenar los datos recibidos

def send_voice_notification(message):
    tts = gTTS(text=message, lang='en')
    tts.save('notification.mp3')
    os.system('mpg123 notification.mp3')  # Asegúrate de tener el reproductor mpg123 instalado

@app.route('/api', methods=['POST'])
def receive_sensor_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    # Verifica las condiciones de notificación
    if temperature < 30 or temperature > 25:
        send_voice_notification("Alerta de temperatura!")

    if humidity < 20 or humidity > 67:
        send_voice_notification("Alerta de humedad!")

    # Almacena los datos en la lista sensor_data
    sensor_data.append({"temperature": temperature, "humidity": humidity})

    return jsonify({"message": "Datos recibidos con éxito"})

@app.route('/data', methods=['GET'])
def get_sensor_data():
    return jsonify(sensor_data)

@app.route('/view', methods=['GET'])
def view_sensor_data():
    return render_template('data.html', sensor_data=sensor_data)

if __name__ == '__main__':
    app.run(host='192.168.33.237', port=5000)
