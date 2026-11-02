#!/bin/bash
# Uso: ./pruebas_curl.sh <API_ID> <STAGE>
# Ejemplo: ./pruebas_curl.sh v6fak03vga dev
API_ID=$1
STAGE=$2
API="https://${API_ID}.execute-api.us-east-1.amazonaws.com/${STAGE}"
BUCKET="fernando-taller3-${STAGE}"   # <-- cámbialo: debe ser único en todo AWS
JSON='Content-Type: application/json'

echo "hola serverless (${STAGE})" > prueba.txt

echo -e "\n== 1) Lista buckets =="
curl -s "$API/s3/lista-buckets"

echo -e "\n\n== 2) Crear bucket =="
curl -s -X POST "$API/s3/bucket/crear" -H "$JSON" -d "{\"bucket\":\"$BUCKET\"}"

echo -e "\n\n== 3) Crear directorio =="
curl -s -X POST "$API/s3/directorio/crear" -H "$JSON" \
  -d "{\"bucket\":\"$BUCKET\",\"directorio\":\"documentos\"}"

echo -e "\n\n== 4) Subir archivo =="
curl -s -X POST "$API/s3/archivo/subir" -H "$JSON" \
  -d "{\"bucket\":\"$BUCKET\",\"directorio\":\"documentos\",\"nombre_archivo\":\"prueba.txt\",\"contenido_base64\":\"$(base64 -w0 prueba.txt)\"}"

echo -e "\n\n== 5) Lista objetos del bucket =="
curl -s -X POST "$API/s3/bucket/lista-objetos" -H "$JSON" -d "{\"bucket\":\"$BUCKET\"}"
echo
