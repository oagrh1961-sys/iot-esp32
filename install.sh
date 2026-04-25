#!/bin/bash
echo "=== Instalando Servidor IoT ==="
sudo apt update && sudo apt install -y python3-venv python3-pip
mkdir -p /home/iot/iot-server/templates
cd /home/iot/iot-server
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic
echo "=== Configurando servicio systemd ==="
sudo cp systemd/iot-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable iot-server
sudo systemctl start iot-server
echo "=== Instalación completa ==="
echo "IP del servidor:"
ip a | grep "inet " | grep -v 127.0.0.1
echo "Dashboard: http://<IP>:8000/dashboard"
