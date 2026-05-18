#!/bin/bash

echo "========================================="
echo " CREANDO DOCKERFILE "
echo "========================================="

cat <<EOF > Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "App.py"]
EOF

echo "========================================="
echo " CONSTRUYENDO IMAGEN DOCKER "
echo "========================================="

docker build -t trekking-app .

echo "========================================="
echo " EJECUTANDO CONTENEDOR "
echo "========================================="

docker run --env-file .env -it trekking-app

echo "========================================="
echo " CONTENEDORES DOCKER "
echo "========================================="

docker ps -a
