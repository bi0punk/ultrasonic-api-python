# arduino-api-python

![CI](https://github.com/bi0punk/arduino-api-python/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue)

Monorepo con dos backends Python para interactuar con placas Arduino/ESP por HTTP:
- **temp-humedad/** — API en Flask que recibe temperatura/humedad, guarda historial y dispara alertas de voz (gTTS) al superar umbrales.
- **distancia/** — API en FastAPI que recibe la distancia medida por un sensor ultrasónico y la muestra en una página web con polling.

## Tabla de contenidos
- [Estructura](#estructura)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [temp-humedad](#temp-humedad)
- [distancia](#distancia)
- [Tests](#tests)
- [CI](#ci)
- [Seguridad](#seguridad)
- [Hardware](#hardware)
- [Licencia](#licencia)

## Estructura
```
arduino-api-python/
├── temp-humedad/        # Flask + gTTS (alertas de voz)
│   ├── main.py
│   ├── Dockerfile
│   ├── templates/data.html
│   ├── hu_edad_ytemp/hu_edad_ytemp.ino   # sketch Arduino
│   └── requirements.txt
├── distancia/           # FastAPI + polling web
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── tests/test_smoke.py  # smoke tests del monorepo
├── .github/workflows/ci.yml
└── ruff.toml
```

## Requisitos previos
- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) (recomendado) o `pip` + `venv`
- Para alertas de voz: `mpg123` instalado en el sistema (`apt install mpg123`)
- Placa Arduino/ESP con el sketch correspondido (ver [Hardware](#hardware))

## Instalación
```bash
git clone https://github.com/bi0punk/arduino-api-python.git
cd arduino-api-python

# Elegí el subproyecto:
cd temp-humedad   # o: cd distancia

uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## temp-humedad
API Flask que recibe datos de un DHT22 y alerta por voz.

### Endpoints
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api` | Recibe `{ "temperature": float, "humidity": float }` |
| `GET` | `/data` | Últimas 1000 lecturas en JSON |
| `GET` | `/view` | Tabla HTML con el historial |

### Umbrales de alerta
- Temperatura: `< 15 °C` o `> 30 °C` → "Alerta de temperatura!"
- Humedad: `< 20 %` o `> 67 %` → "Alerta de humedad!"

### Correr
```bash
cd temp-humedad
uv run python main.py            # 0.0.0.0:5000
# Variables: HOST, PORT
```

### Docker
```bash
docker build -t temp-humedad ./temp-humedad
docker run -p 5000:5000 temp-humedad
```

## distancia
API FastAPI que recibe la distancia de un sensor ultrasónico (HC-SR04) y la muestra en una web con polling cada 1s.

### Endpoints
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/data` | Recibe `{ "distance": float }` |
| `GET` | `/` | Página HTML con polling |
| `GET` | `/get_latest_data` | Última distancia en JSON |

### Correr
```bash
cd distancia
uv run uvicorn app:app --host 0.0.0.0 --port 8080
# Variable: CORS_ORIGINS (csv, default http://localhost:8080)
```

### Docker
```bash
docker build -t distancia ./distancia
docker run -p 8080:8080 distancia
```

## Tests
Smoke tests que validan estructura del repo, imports de ambas apps y que no haya venv commiteado:
```bash
uv venv && source .venv/bin/activate
uv pip install -r temp-humedad/requirements.txt -r distancia/requirements.txt pytest
pytest -q
```

## CI
`.github/workflows/ci.yml` corre por cada subproyecto (matrix `temp-humedad`, `distancia`):
- `ruff check` + `ruff format --check`
- smoke tests del repo raíz.

## Seguridad
- **CORS** (`distancia/`): orígenes configurables por `CORS_ORIGINS`, `allow_credentials=False`. No se usa `*` con credenciales.
- **temp-humedad**: escucha en `0.0.0.0` para uso en contenedor/LAN; usar detrás de un proxy/reverse-proxy en producción.
- Sin secretos hardcodeados; credenciales de red WiFi van en el sketch `.ino` (fuera de este repo si los compartís).

## Hardware
- **temp-humedad**: Arduino + DHT22 (temperatura/humedad). Sketch en `temp-humedad/hu_edad_ytemp/hu_edad_ytemp.ino`.
- **distancia**: Wemos D1 mini + HC-SR04 (ultrasonido). El POST va a `/data` con el campo `distance` en cm.

## Licencia
MIT — ver [LICENSE](LICENSE).
