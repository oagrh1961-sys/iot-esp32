# 🌡️ IoT ESP32 + DHT11 — Servidor FastAPI con Dashboard Web

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite)
![ESP32](https://img.shields.io/badge/ESP32-Arduino-red?logo=arduino)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-orange?logo=ubuntu)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Descripción

Proyecto IoT completo que conecta un microcontrolador **ESP32** con un sensor de temperatura y humedad **DHT11** a un servidor backend **FastAPI** corriendo en una máquina virtual Ubuntu. Los datos se almacenan en **SQLite** y **CSV**, y se visualizan en un **dashboard web** con gráficas en tiempo real.

---

## 🏗️ Arquitectura

```
[ESP32 + DHT11] → HTTP POST → [Ubuntu VM FastAPI] → SQLite + CSV → Dashboard Web
```

| Componente | Rol |
|---|---|
| ESP32 + DHT11 | Sensor de temperatura y humedad, envía datos cada 5 segundos |
| WiFi | Transporte HTTP entre el ESP32 y el servidor |
| FastAPI (Python) | Servidor REST que recibe, almacena y expone los datos |
| SQLite | Base de datos embebida para almacenamiento persistente |
| CSV | Exportación de datos en formato plano |
| Dashboard Web | Visualización con gráficas y tabla en tiempo real |
| Ubuntu 22.04 (VM) | Sistema operativo del servidor en VirtualBox |

---

## 🧰 Tecnologías utilizadas

| Tecnología | Versión | Uso |
|---|---|---|
| ESP32 | — | Microcontrolador principal |
| DHT11 | — | Sensor temperatura/humedad |
| Python | 3.10+ | Lenguaje del servidor |
| FastAPI | 0.136.x | Framework REST API |
| SQLite | 3 | Base de datos local |
| SQLAlchemy | 2.0.x | ORM para SQLite |
| Uvicorn | 0.46.x | Servidor ASGI |
| Chart.js | CDN | Gráficas en el dashboard |
| Ubuntu | 22.04 | Sistema operativo (VM) |
| VirtualBox | 7.x | Virtualización |

---

## 📁 Estructura del proyecto

```
iot-esp32/
├── README.md
├── install.sh                      # Script de instalación automática
├── .gitignore
│
├── server/
│   ├── main.py                     # Servidor FastAPI
│   ├── requirements.txt            # Dependencias Python
│   └── templates/
│       └── index.html              # Dashboard web
│
├── esp32/
│   ├── esp32_dht11.ino             # Sketch Arduino para ESP32
│   └── credentials.h.example      # Plantilla de credenciales WiFi
│
└── systemd/
    └── iot-server.service          # Servicio systemd (autostart)
```

---

## 🚀 Instalación paso a paso en Ubuntu 22.04

### Requisitos previos

- Ubuntu 22.04 LTS (físico o VM en VirtualBox)
- Python 3.10+
- Acceso a internet

### 1. Clonar el repositorio

```bash
git clone https://github.com/oagrh1961-sys/iot-esp32.git
cd iot-esp32
```

### 2. Instalar dependencias del sistema

```bash
sudo apt update && sudo apt install -y python3-venv python3-pip
```

### 3. Crear entorno virtual e instalar dependencias Python

```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Iniciar el servidor

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Acceder al dashboard

Abre en tu navegador:

```
http://<IP_DEL_SERVIDOR>:8000/dashboard
```

### 6. Instalación automática (script)

```bash
chmod +x install.sh
./install.sh
```

---

## 📡 Endpoints de la API

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Estado del servidor |
| `GET` | `/dashboard` | Dashboard web (HTML) |
| `POST` | `/datos` | Recibir dato del ESP32 |
| `GET` | `/datos` | Listar todos los datos |
| `GET` | `/datos/ultimo` | Último dato registrado |
| `GET` | `/csv` | Ver datos del archivo CSV |

### Ejemplo POST `/datos`

```json
{
  "temperatura": 24.5,
  "humedad": 62.0,
  "dispositivo": "ESP32-01"
}
```

### Respuesta

```json
{
  "mensaje": "Dato guardado en DB y CSV",
  "id": 42
}
```

---

## 🔌 Configuración del ESP32

### 1. Credenciales WiFi

Copia el archivo de ejemplo y edítalo:

```bash
cd esp32
cp credentials.h.example credentials.h
```

Edita `credentials.h`:

```cpp
const char* ssid     = "NOMBRE_DE_TU_WIFI";
const char* password = "CONTRASEÑA_WIFI";
```

### 2. IP del servidor

En `esp32_dht11.ino`, cambia la IP del servidor:

```cpp
const char* serverUrl = "http://192.168.1.100:8000/datos";
```

### 3. Librerías necesarias (Arduino IDE)

- `DHT sensor library` (Adafruit)
- `ArduinoJson`
- `WiFi` (incluida en ESP32 board package)
- `HTTPClient` (incluida en ESP32 board package)

---

## 🌐 Configurar red en VirtualBox (Adaptador Puente)

Para que el ESP32 pueda comunicarse con la VM, la red debe estar en modo **Adaptador Puente**:

1. Apaga la VM
2. Ve a **Configuración → Red**
3. En **Adaptador 1**, cambia a: **Adaptado puente (Bridged Adapter)**
4. Selecciona tu interfaz de red física (WiFi o Ethernet)
5. Inicia la VM
6. Verifica la IP con:

```bash
ip a | grep "inet " | grep -v 127.0.0.1
```

---

## 🗄️ Ver historial con sqlite3

```bash
cd server
sqlite3 iot_datos.db
```

Comandos útiles:

```sql
-- Listar todos los datos
SELECT * FROM datos;

-- Últimos 10 registros
SELECT * FROM datos ORDER BY id DESC LIMIT 10;

-- Salir
.quit
```

---

## ⚙️ Servicio autostart con systemd

El archivo `systemd/iot-server.service` configura el servidor para iniciarse automáticamente al arrancar Ubuntu.

```bash
sudo cp systemd/iot-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable iot-server
sudo systemctl start iot-server
```

Verificar estado:

```bash
sudo systemctl status iot-server
```

Ver logs en tiempo real:

```bash
journalctl -u iot-server -f
```

---

## 📝 Notas importantes

> ⚠️ **La IP del servidor puede cambiar** si se reasigna por DHCP. Para evitarlo, asigna una IP estática en tu router o en Ubuntu (`/etc/netplan/`).

> ✅ El servicio systemd (`iot-server.service`) reinicia automáticamente el servidor si falla (`Restart=always`).

> 🔒 El archivo `credentials.h` está en `.gitignore` para no exponer tus contraseñas WiFi. Nunca lo subas al repositorio.

---

## 👤 Autor

**oagrh1961-sys**  
GitHub: [@oagrh1961-sys](https://github.com/oagrh1961-sys)

---

*Proyecto IoT educativo — ESP32 + DHT11 + FastAPI + SQLite + Dashboard Web*
