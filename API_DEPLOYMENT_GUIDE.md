# KATA Testing API - Deployment Guide

## ✅ Current Status

### Local API Server (WORKING)
- **URL:** `http://localhost:8000`
- **Status:** ✅ Fully functional
- **Data Source:** Azure Blob Storage (`katauploads/kata-reports/degraded_responses.xlsx`)

### Azure Deployment (IN PROGRESS)
- **App Service:** kata-api-v2.azurewebsites.net
- **Status:** ⚠️ Deployed but experiencing startup issues
- **Next Steps:** Troubleshooting startup configuration

---

## 🚀 Quick Start - Frontend Team

### Option 1: Local API (Immediate Use)

The API server is running locally and fully functional:

```bash
# Base URL
http://localhost:8000

# API Endpoints
GET  /                                      # API information
GET  /api/health                            # Health check + Blob Storage status
GET  /api/degraded-responses                # All degraded responses (all sheets)
GET  /api/degraded-responses/PSP            # PSP Mentor prompts only
GET  /api/degraded-responses/VSM            # VSM Mentor prompts only
GET  /api/degraded-responses/TPI            # TPI Mentor prompts only
POST /api/refresh                           # Force cache refresh
GET  /docs                                  # Interactive API documentation
GET  /redoc                                 # Alternative API documentation
```

### Option 2: Expose Local API Externally (Using ngrok)

To make the local API accessible to your frontend team:

```bash
# Install ngrok (if not installed)
brew install ngrok

# Start ngrok tunnel
ngrok http 8000

# You'll get a public URL like: https://xxxx-xx-xx-xx-xx.ngrok-free.app
# Share this URL with frontend team
```

### Option 3: Azure Deployment (Recommended for Production)

**URL:** `https://kata-api-v2.azurewebsites.net`  
**Status:** Currently troubleshooting startup

---

## 📊 API Response Format

### GET /api/degraded-responses

Returns JSON with all sheets:

```json
{
  "total_sheets": 3,
  "last_updated": "2026-02-12T22:28:13.307954",
  "sheets": {
    "PSP Mentor Prompts": {
      "sheet_name": "PSP Mentor Prompts",
      "row_count": 44,
      "data": [
        {
          "SL": "1",
          "Prompts": "How do I identify if a problem is caused or created?",
          "Response": "...",
          "Sources": "...",
          "Status": "Bad",
          "Tester Remarks": "...",
          "Developer Remarks": null,
          "Date": null
        }
      ]
    },
    "VSM Mentor Prompts": { ... },
    "TPI Mentor Prompts": { ... }
  }
}
```

### GET /api/degraded-responses/PSP

Returns only PSP sheet data:

```json
{
  "sheet_name": "PSP Mentor Prompts",
  "row_count": 44,
  "data": [ ... ]
}
```

---

## 🔄 Data Flow

1. **Testing Script** (`integrated_test_comparison.py`)
   - Tests API responses against benchmarks
   - Identifies degraded responses
   - Generates `Degraded_Responses_Report.xlsx`
   - Uploads to Azure Blob Storage as `degraded_responses.xlsx`

2. **Azure Blob Storage**
   - Storage Account: `katauploads`
   - Container: `kata-reports`
   - File: `degraded_responses.xlsx`

3. **FastAPI Server** (`api_server.py`)
   - Downloads Excel from Blob Storage
   - Converts to JSON
   - Caches for 5 minutes
   - Serves via REST API

4. **Frontend**
   - Fetches JSON from API
   - Displays in tabular format

---

## 🛠️ Running the API Server Locally

### Prerequisites
```bash
cd /Users/abhay.manikanti/Downloads/KataTestingFramework-main
pip install -r requirements.txt
```

### Start Server
```bash
# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Start server
python3 api_server.py
```

Or use the startup script:
```bash
./start_server.sh
```

### Test Server
```bash
# Health check
curl http://localhost:8000/api/health | python3 -m json.tool

# Get all data
curl http://localhost:8000/api/degraded-responses | python3 -m json.tool | head -50

# Get specific sheet
curl http://localhost:8000/api/degraded-responses/PSP | python3 -m json.tool | head -50
```

---

## 🧪 Generate Fresh Test Data

To upload new degraded responses:

```bash
# Run the integrated test
python3 integrated_test_comparison.py

# This will:
# 1. Test all API responses
# 2. Compare with benchmarks
# 3. Generate Degraded_Responses_Report.xlsx
# 4. Upload to Azure Blob Storage as degraded_responses.xlsx
# 5. API will automatically serve the new data (cache refreshes every 5 min)
```

---

## 🐳 Azure Deployment

### Current Deployment
- **Resource Group:** rg-kata-v2
- **App Service:** kata-api-v2
- **Runtime:** Python 3.11
- **Region:** East US

### Environment Variables Set
```
AZURE_STORAGE_CONNECTION_STRING = <configured>
```

### Troubleshooting Azure Deployment

Check logs:
```bash
az webapp log tail --name kata-api-v2 --resource-group rg-kata-v2
```

Restart app:
```bash
az webapp restart --name kata-api-v2 --resource-group rg-kata-v2
```

---

## 📝 Frontend Integration Example

### JavaScript/TypeScript
```typescript
const API_BASE_URL = 'http://localhost:8000'; // or ngrok URL

// Fetch all degraded responses
async function getAllDegradedResponses() {
  const response = await fetch(`${API_BASE_URL}/api/degraded-responses`);
  const data = await response.json();
  return data;
}

// Fetch specific sheet
async function getPSPResponses() {
  const response = await fetch(`${API_BASE_URL}/api/degraded-responses/PSP`);
  const data = await response.json();
  return data;
}

// Health check
async function checkAPIHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  const status = await response.json();
  console.log('API Status:', status.status);
  console.log('Blob Connected:', status.blob_storage.connected);
}
```

### Python
```python
import requests

API_BASE_URL = 'http://localhost:8000'

# Get all data
response = requests.get(f'{API_BASE_URL}/api/degraded-responses')
data = response.json()

# Get specific sheet
psp_data = requests.get(f'{API_BASE_URL}/api/degraded-responses/PSP').json()

# Health check
health = requests.get(f'{API_BASE_URL}/api/health').json()
print(f"API Status: {health['status']}")
```

---

## 🔐 Security Notes

- The connection string is sensitive - currently in `.env` file (not in git)
- For production, use Azure Key Vault or managed identities
- Enable CORS properly for production domains
- Current CORS setting allows all origins (`*`) - restrict in production

---

## 📞 Support

For issues or questions:
1. Check API health: `GET /api/health`
2. Review server logs: `cat /tmp/api_server.log`
3. Verify Blob Storage connection string
4. Ensure Excel file exists in Blob Storage

---

## ✅ Next Steps for Frontend Team

### Immediate (Today)
1. Use local API: `http://localhost:8000`
2. Test endpoints with the examples above
3. Confirm JSON structure meets your needs

### Short-term (This Week)
1. Use ngrok for external access if needed
2. We'll complete Azure deployment troubleshooting
3. Provide production URL: `https://kata-api-v2.azurewebsites.net`

### Questions?
- API structure unclear? Check `/docs` endpoint
- Need different data format? Let us know
- Need additional endpoints? We can add them

---

**Last Updated:** February 12, 2026  
**Maintained By:** KATA Testing Team
