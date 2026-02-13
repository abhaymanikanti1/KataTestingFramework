# Quick Deployment with ngrok

## 🚀 Instant Public URL for Frontend Team

Since Azure App Service is experiencing startup issues, use ngrok to expose your local API publicly:

### Step 1: Install ngrok
```bash
brew install ngrok
```

### Step 2: Start Your API Server
```bash
cd /Users/abhay.manikanti/Downloads/KataTestingFramework-main
./start_api_for_frontend.sh
```

### Step 3: Start ngrok Tunnel
```bash
# In a new terminal
ngrok http 8000
```

### Step 4: Get Your Public URL
ngrok will display something like:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000
```

**Give this URL to your frontend team:** `https://abc123.ngrok-free.app`

### Step 5: Test It
```bash
curl https://abc123.ngrok-free.app/api/health
curl https://abc123.ngrok-free.app/api/degraded-responses
```

## 🎯 Frontend Team Usage

Replace `http://localhost:8000` with your ngrok URL:

```javascript
const API_URL = 'https://abc123.ngrok-free.app';

fetch(`${API_URL}/api/degraded-responses`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## ⚡ Benefits
- ✅ Works immediately (no Azure config needed)
- ✅ HTTPS enabled automatically
- ✅ Free for development/testing
- ✅ Same API, just different URL

## 📝 Notes
- ngrok URL changes each time you restart (unless you have a paid account)
- Keep your terminal/computer running while frontend team tests
- For permanent deployment, we'll fix Azure App Service separately

## 🔄 When to Use
- **Now:** For immediate frontend team access
- **Later:** Switch to Azure when deployment is stable
