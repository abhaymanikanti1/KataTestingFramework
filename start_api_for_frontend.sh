#!/bin/bash
# Start KATA Testing API Server for Frontend Access

echo "======================================================================"
echo "🚀 Starting KATA Testing API Server"
echo "======================================================================"
echo ""

# Load Azure Storage connection string from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Change to script directory
cd "$(dirname "$0")"

# Check if server is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Server already running on port 8000"
    echo ""
    echo "To stop it: pkill -f api_server.py"
    echo "Then run this script again"
    exit 1
fi

# Start the server
echo "📡 Starting server on http://0.0.0.0:8000"
echo ""
echo "Available endpoints:"
echo "  - http://localhost:8000/              (API info)"
echo "  - http://localhost:8000/api/health    (Health check)"
echo "  - http://localhost:8000/api/degraded-responses  (All data)"
echo "  - http://localhost:8000/docs          (Interactive docs)"
echo ""
echo "To stop: Press Ctrl+C or run: pkill -f api_server.py"
echo "======================================================================"
echo ""

python3 api_server.py
