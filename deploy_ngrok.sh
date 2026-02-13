#!/bin/bash
# Quick deploy script using ngrok

echo "=========================================="
echo "🚀 KATA API - Quick Deployment"
echo "=========================================="
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok not found"
    echo ""
    echo "Install ngrok:"
    echo "  brew install ngrok"
    echo ""
    echo "Or download from: https://ngrok.com/download"
    exit 1
fi

# Check if API server is running
if ! lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  API server not running on port 8000"
    echo ""
    echo "Starting API server..."
    cd "$(dirname "$0")"
    ./start_api_for_frontend.sh &
    sleep 10
    echo ""
fi

# Start ngrok
echo "✅ Starting ngrok tunnel..."
echo ""
echo "=========================================="
echo "📡 Your Public API URL:"
echo "=========================================="
echo ""
echo "ngrok will display your public URL below."
echo "Look for the 'Forwarding' line with https://"
echo ""
echo "Give that URL to your frontend team!"
echo ""
echo "Example: https://abc123.ngrok-free.app"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================================="
echo ""

ngrok http 8000
