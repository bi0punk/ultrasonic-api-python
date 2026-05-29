# distancia-wemos

FastAPI web server that receives distance sensor (ultrasonic) data from a Wemos/Arduino board via HTTP POST, stores the latest value, and displays it on a live web page with Bootstrap styling.

## Stack

Python 3, FastAPI, Uvicorn, Bootstrap, Docker

## Usage

```bash
pip install -r requirements.txt
python app.py
```

Or with Docker:
```bash
docker compose up
```

## API

- `POST /data` — Receive sensor reading `{"distance": 123}`
- `GET /` — Live web dashboard

## License

MIT
