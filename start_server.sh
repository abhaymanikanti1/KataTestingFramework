#!/bin/bash
# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi
cd /Users/abhay.manikanti/Downloads/KataTestingFramework-main
python3 api_server.py
