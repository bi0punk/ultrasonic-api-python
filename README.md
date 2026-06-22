# ultrasonic-api-python

FastAPI web server with Socket.IO that serves a real-time dashboard displaying ultrasonic distance sensor data received via HTTP POST.

**Security:** CORS restricted to localhost by default. Use environment variables to configure allowed origins for production.

## Stack

Python 3, FastAPI, Socket.IO, Docker

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
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

## Configuration

| Variable | Default | Description |
|---|---|---|
| `CORS_ORIGINS` | `http://localhost:8000` | Allowed CORS origins (comma-separated) |

## Security

- Socket.IO CORS restricted to `http://localhost:8000` by default
- No authentication on endpoints (intended for LAN use only)
- Use a reverse proxy with HTTPS and authentication for internet-facing deployments

## License

MIT
