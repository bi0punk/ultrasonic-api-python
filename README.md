# temp-humedad-python

Flask application that receives temperature and humidity sensor data via API, stores it, and triggers voice alerts (gTTS) when thresholds are exceeded.

## Stack

Python 3, Flask, gTTS (Google Text-to-Speech)

## Installation

```bash
pip install flask gtts
```

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api` | Receive sensor data (temperature, humidity) |
| GET | `/data` | JSON sensor history |
| GET | `/view` | HTML template data viewer |

## License

MIT
