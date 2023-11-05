from flask import Flask, request, jsonify

app = Flask(__name__)

sensor_data = []  # Lista para almacenar los datos recibidos

@app.route('/api', methods=['POST'])
def receive_sensor_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    # Almacena los datos en la lista sensor_data
    sensor_data.append({"temperature": temperature, "humidity": humidity})

    return jsonify({"message": "Datos recibidos con éxito"})

@app.route('/data', methods=['GET'])
def get_sensor_data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(host='192.168.33.237', port=5000)
