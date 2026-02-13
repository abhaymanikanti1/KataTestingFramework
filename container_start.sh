#!/bin/bash
pip install --no-cache-dir fastapi uvicorn openpyxl azure-storage-blob pandas
uvicorn api_server:app --host 0.0.0.0 --port 8000
