#!/bin/bash
# Fix Azure App Service startup

echo "Configuring Azure App Service startup..."

# Set proper startup command for Python 3.11
az webapp config set \
  --resource-group rg-kata-v2 \
  --name kata-api-v2 \
  --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker api_server:app --bind=0.0.0.0:8000 --timeout 600"

echo "Restarting app..."
az webapp restart --resource-group rg-kata-v2 --name kata-api-v2

echo "Waiting 30 seconds for startup..."
sleep 30

echo "Testing..."
curl -I https://kata-api-v2.azurewebsites.net/

echo ""
echo "If still not working, try:"
echo "1. Check logs: az webapp log tail --name kata-api-v2 --resource-group rg-kata-v2"
echo "2. Use local API: http://localhost:8000"
