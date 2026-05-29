# ultrasonic-api-python

FastAPI web server with Socket.IO that serves a real-time dashboard displaying ultrasonic distance sensor data received via HTTP POST.

## Stack

Python 3, FastAPI, Socket.IO, Docker

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Or with Docker:
```bash
docker build -t ultrasonic-api .
docker run -p 8000:8000 ultrasonic-api
```

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/data` | Receive sensor reading |
| GET | `/` | Live HTML dashboard |
| GET | `/get_latest_data` | Latest reading as JSON |

## License

MIT
