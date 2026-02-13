# Kata Testing Framework

## Overview

Automated API quality testing framework that:
1. **Tests** 4 AI mentor APIs (PSP, VSM, TPI, Search/Chat) against benchmark data
2. **Compares** responses to detect quality degradation
3. **Uploads** results to Azure Blob Storage & SharePoint
4. **Serves** data as JSON via FastAPI for frontend consumption
5. **Alerts** teams via Microsoft Teams webhooks
6. **Runs** automatically via GitHub Actions (daily at 8:00 AM IST)

---

## 🚀 Quick Start

### For Backend Setup (Testing & API)

See **[QUICKSTART.md](QUICKSTART.md)** - Get running in 10 minutes!

### For Frontend Integration

Your frontend team can call:
```typescript
const response = await fetch('http://your-api-url/api/degraded-responses');
const data = await response.json();
// data.sheets[0].data = array of degraded responses
```

See **[frontend_examples.py](frontend_examples.py)** for React/Vue/TypeScript code.

---

## 📋 What's Included

### Core Testing System
- **`integrated_test_comparison.py`** - Main testing script
  - Sends questions to 4 AI mentors
  - Compares with benchmark responses in `compare.xlsx`
  - Detects degradation (errors, shorter responses, missing keywords)
  - Generates Excel report with degraded responses
  - Uploads to Blob Storage & SharePoint
  - Sends Teams alerts

### API Server (New!)
- **`api_server.py`** - FastAPI server
  - Reads Excel from Azure Blob Storage
  - Converts to JSON format
  - Caches data (5-minute refresh)
  - Serves via REST API
  - Interactive docs at `/docs`

### Blob Storage Integration (New!)
- **`blob_storage_uploader.py`** - Azure Blob Storage client
  - Uploads Excel files
  - Downloads for API server
  - Overwrites existing (always latest version)

### Deployment
- **`Dockerfile`** - Container build config
- **`docker-compose.yml`** - Local dev setup
- **`.github/workflows/daily-kata-test.yml`** - GitHub Actions workflow

### Documentation
- **`QUICKSTART.md`** - 10-minute setup guide
- **`FRONTEND_API_SETUP_GUIDE.md`** - Complete API setup & deployment
- **`AZURE_BLOB_STORAGE_SETUP.md`** - Blob Storage deep dive
- **`SETUP_SUMMARY.md`** - Architecture overview

---

## 🏗️ Architecture

```
┌──────────────────────┐
│  Testing Script      │  Runs daily via GitHub Actions
│  (Python)            │  Tests 4 AI mentors
└──────────┬───────────┘
           │ Uploads Excel
           ▼
┌──────────────────────┐
│  Azure Blob Storage  │  Stores Degraded_Responses_Report.xlsx
└──────────┬───────────┘  (Latest version, overwrite mode)
           │ Read by API
           ▼
┌──────────────────────┐
│  FastAPI Server      │  Converts Excel → JSON
│  (Python)            │  Caches for 5 minutes
└──────────┬───────────┘  Serves via REST API
           │ GET /api/degraded-responses
           ▼
┌──────────────────────┐
│  Frontend            │  Displays table/dashboard
│  (React/Vue/etc)     │  Gets clean JSON data
└──────────────────────┘
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/api/health` | GET | Health check |
| `/api/degraded-responses` | GET | All degraded responses |
| `/api/degraded-responses/{sheet_name}` | GET | Specific sheet |
| `/api/refresh` | POST | Force cache refresh |
| `/docs` | GET | Interactive API docs |

Example response:
```json
{
  "total_sheets": 4,
  "total_issues": 15,
  "last_updated": "2026-02-12T10:30:00",
  "sheets": [
    {
      "sheet_name": "PSP Mentor",
      "row_count": 5,
      "data": [
        {
          "Serial Number": "5",
          "Prompt": "What is DIVE?",
          "Severity": "HIGH",
          "Degradation Reason": "Response 60% shorter"
        }
      ]
    }
  ]
}
```

---

## ⚙️ Setup

### Prerequisites
- Python 3.11+
- Azure account (for Blob Storage)
- Azure Storage Account with container `kata-reports`

### Installation

```bash
# Clone repo
cd KataTestingFramework-main

# Install dependencies
pip install -r requirements.txt

# Set Azure connection string
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net"

# Test upload
python integrated_test_comparison.py

# Start API server
python api_server.py

# Visit API docs
open http://localhost:8000/docs
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Required for API & Upload
AZURE_STORAGE_CONNECTION_STRING="your-connection-string"

# Optional (keep existing functionality)
TEAMS_WEBHOOK_URL="your-teams-webhook-url"
SHAREPOINT_UPLOAD_URL="your-sharepoint-url"
```

### GitHub Actions Secrets

Add these in: Settings → Secrets and variables → Actions

- `AZURE_STORAGE_CONNECTION_STRING`
- `TEAMS_WEBHOOK_URL`
- `SHAREPOINT_UPLOAD_URL` (optional)

---

## 🚢 Deployment

### Local Development

```bash
# Run with Docker Compose
docker-compose up
```

### Azure Container Instances

```bash
az container create \
  --name kata-api \
  --resource-group kata-testing-rg \
  --image yourregistry.azurecr.io/kata-api \
  --dns-name-label kata-api \
  --ports 8000 \
  --environment-variables \
    AZURE_STORAGE_CONNECTION_STRING="your-string"
```

### Azure App Service

```bash
az webapp up \
  --name kata-api \
  --runtime PYTHON:3.11 \
  --sku B1

az webapp config appsettings set \
  --name kata-api \
  --settings AZURE_STORAGE_CONNECTION_STRING="your-string"
```

---

## 🧪 Testing

### Run Tests Locally

```bash
# Full test (all questions)
python integrated_test_comparison.py

# Test upload only
python blob_storage_uploader.py

# Test API server
python api_server.py
# Then visit: http://localhost:8000/docs
```

### Frontend Integration Test

```bash
# Start API server
python api_server.py

# In another terminal, test endpoint
curl http://localhost:8000/api/degraded-responses | jq
```

---

## 📁 File Structure

```
KataTestingFramework-main/
├── integrated_test_comparison.py   # Main testing script
├── blob_storage_uploader.py        # Azure Blob Storage client
├── api_server.py                   # FastAPI server
├── compare.xlsx                    # Benchmark data
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container build
├── docker-compose.yml              # Local dev setup
├── .github/workflows/              # GitHub Actions
│   └── daily-kata-test.yml
├── frontend_examples.py            # Frontend code examples
├── QUICKSTART.md                   # Fast setup guide
├── FRONTEND_API_SETUP_GUIDE.md     # Complete guide
├── AZURE_BLOB_STORAGE_SETUP.md     # Blob Storage guide
├── SETUP_SUMMARY.md                # Architecture overview
└── README.md                       # This file
```

---

## 💰 Cost Estimate

| Service | Cost |
|---------|------|
| Azure Blob Storage (1GB) | $0.02/month |
| Container Instance (1 vCPU, 1.5GB RAM) | $15/month |
| App Service (B1) | $13/month |

**Total: ~$15-20/month**

---

## 🔄 Workflow

### Daily Automation (GitHub Actions)

1. **8:00 AM IST** - GitHub Actions triggers
2. **Test APIs** - Runs all 4 mentors (PSP, VSM, TPI, Search)
3. **Compare** - Checks against benchmark in `compare.xlsx`
4. **Detect Issues** - Flags degraded responses
5. **Generate Report** - Creates Excel with issues
6. **Upload** - Sends to Azure Blob Storage & SharePoint
7. **Alert** - Posts to Teams if issues found
8. **API Auto-Updates** - Next frontend call gets latest data

### Manual Run

```bash
# Run tests immediately
python integrated_test_comparison.py

# Force API to refresh cache
curl -X POST http://your-api-url/api/refresh
```

---

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 10 minutes
- **[FRONTEND_API_SETUP_GUIDE.md](FRONTEND_API_SETUP_GUIDE.md)** - Full setup & deployment
- **[frontend_examples.py](frontend_examples.py)** - React/Vue/TypeScript examples
- **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Architecture & overview

---

## 🤝 Frontend Integration

### For Frontend Developers

1. **API Base URL**: `http://your-deployed-api-url`

2. **Main Endpoint**: `GET /api/degraded-responses`

3. **Response Format**: See `/docs` for interactive examples

4. **Code Examples**: 
   - TypeScript: `frontend_examples.py` → TypeScript section
   - React: `frontend_examples.py` → React section
   - Vue: `frontend_examples.py` → Vue section

5. **API Docs**: `http://your-api-url/docs` (Swagger UI)

---

## 🐛 Troubleshooting

### "AZURE_STORAGE_CONNECTION_STRING not set"

```bash
export AZURE_STORAGE_CONNECTION_STRING="your-connection-string"
```

### API returns 503

Excel file doesn't exist yet. Run:
```bash
python integrated_test_comparison.py
```

### CORS errors

Update `api_server.py`:
```python
allow_origins=["https://yourfrontend.com"]
```

### Upload fails

Check connection string is valid:
```bash
python -c "from blob_storage_uploader import check_blob_exists; print(check_blob_exists())"
```

---

## 📝 License

[Your License Here]

---

## 👥 Contact

Owner: Abhay Manikanti (abhay.manikanti@fortive.com)

For support:
1. Check documentation in this repo
2. Test locally following QUICKSTART.md
3. Check API docs at `/docs` endpoint
4. Review error messages in terminal/logs
