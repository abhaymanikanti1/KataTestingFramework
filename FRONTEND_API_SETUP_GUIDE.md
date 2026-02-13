# Frontend API Setup Guide: Excel Data as JSON via FastAPI

## Architecture Overview

```
┌─────────────────────┐
│  Testing Script     │
│  (Python)           │
└──────┬──────────────┘
       │ 1. Upload Excel
       ▼
┌─────────────────────┐
│  Azure Blob Storage │
│  (File Storage)     │
└──────┬──────────────┘
       │ 2. Read Excel
       ▼
┌─────────────────────┐
│  FastAPI Server     │
│  (Convert to JSON)  │
└──────┬──────────────┘
       │ 3. GET /api/degraded-responses
       ▼
┌─────────────────────┐
│  Frontend (React)   │
│  (Display Table)    │
└─────────────────────┘
```

**Benefits:**
- ✅ Frontend gets clean JSON data via simple API call
- ✅ No Excel parsing on frontend
- ✅ Single source of truth (Blob Storage)
- ✅ Fast, scalable, and cost-effective

---

## Part 1: Azure Setup (5 minutes)

### Step 1: Create Storage Account

1. Go to: https://portal.azure.com
2. Search: **"Storage accounts"** → Click **+ Create**
3. Fill in:
   - **Resource Group:** `kata-testing-rg` (create new)
   - **Storage account name:** `katatestingstorage` (must be unique globally)
   - **Region:** `East US`
   - **Performance:** `Standard`
   - **Redundancy:** `LRS` (cheapest)
4. Click: **Review + Create** → **Create**
5. Wait ~1 minute for deployment

### Step 2: Create Container

1. Go to your storage account → **Containers** (left menu)
2. Click: **+ Container**
3. Name: `kata-reports`
4. Public access level: **Private** (recommended)
5. Click: **Create**

### Step 3: Get Connection String

1. Storage account → **Access keys** (left menu)
2. Click: **Show keys**
3. Copy **Connection string** under **key1**
4. Save it securely - format:
   ```
   DefaultEndpointsProtocol=https;AccountName=katatestingstorage;AccountKey=xxxxx;EndpointSuffix=core.windows.net
   ```

---

## Part 2: Install Dependencies

Update `requirements.txt`:

```txt
PyPDF2>=3.0.0
openpyxl>=3.1.0
requests>=2.31.0
azure-storage-blob>=12.19.0
fastapi>=0.109.0
uvicorn>=0.27.0
python-multipart>=0.0.6
pandas>=2.2.0
```

Install:
```bash
pip install -r requirements.txt
```

---

## Part 3: Upload Script (Update Existing Code)

Create `blob_storage_uploader.py`:

```python
"""
Azure Blob Storage Upload Module
Uploads Excel files to Azure Blob Storage
"""
from azure.storage.blob import BlobServiceClient
import os
from datetime import datetime

# Configuration
CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = 'kata-reports'
BLOB_NAME = 'Degraded_Responses_Report.xlsx'  # Fixed filename - overwrites

def upload_excel_to_blob(local_file_path, blob_name=BLOB_NAME):
    """
    Upload Excel file to Azure Blob Storage
    - Overwrites existing file with same name
    - Returns blob URL
    """
    if not CONNECTION_STRING:
        print("\n  ⚠️  AZURE_STORAGE_CONNECTION_STRING not set")
        return None
    
    if not os.path.exists(local_file_path):
        print(f"\n  ⚠️  File not found: {local_file_path}")
        return None
    
    try:
        print(f"\n  📤 Uploading {os.path.basename(local_file_path)} to Azure Blob Storage...")
        
        # Create clients
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_client = container_client.get_blob_client(blob_name)
        
        # Upload file (overwrite if exists)
        with open(local_file_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        
        blob_url = blob_client.url
        file_size = os.path.getsize(local_file_path)
        
        print(f"  ✅ Upload successful!")
        print(f"  📁 File size: {file_size:,} bytes")
        print(f"  🔗 Blob URL: {blob_url}")
        
        return blob_url
        
    except Exception as e:
        print(f"\n  ❌ Error uploading to Blob Storage: {e}")
        import traceback
        traceback.print_exc()
        return None

def download_excel_from_blob(blob_name=BLOB_NAME, local_file_path=None):
    """
    Download Excel file from Azure Blob Storage
    - For API server to read latest data
    """
    if not CONNECTION_STRING:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING not set")
    
    if local_file_path is None:
        local_file_path = f"/tmp/{blob_name}"
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(CONTAINER_NAME, blob_name)
        
        with open(local_file_path, 'wb') as download_file:
            download_file.write(blob_client.download_blob().readall())
        
        return local_file_path
        
    except Exception as e:
        print(f"Error downloading from Blob Storage: {e}")
        return None

# Test the upload
if __name__ == "__main__":
    test_file = "Degraded_Responses_Report.xlsx"
    
    if os.path.exists(test_file):
        url = upload_excel_to_blob(test_file)
        if url:
            print(f"\n✅ Success! File uploaded to: {url}")
    else:
        print(f"❌ Test file not found: {test_file}")
        print("Run integrated_test_comparison.py first to generate the report.")
```

---

## Part 4: FastAPI Server

Create `api_server.py`:

```python
"""
FastAPI Server for Degraded Responses Data
Serves Excel data as JSON for frontend consumption
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import openpyxl
from datetime import datetime
import os
from blob_storage_uploader import download_excel_from_blob, BLOB_NAME

app = FastAPI(
    title="KATA Testing API",
    description="API for degraded responses data",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache for Excel data (refresh every 5 minutes)
data_cache = {
    'data': None,
    'last_updated': None,
    'cache_duration': 300  # 5 minutes in seconds
}

def read_excel_from_blob():
    """
    Download Excel from Blob Storage and parse into JSON
    """
    try:
        # Download from Blob Storage
        local_file = download_excel_from_blob()
        
        if not local_file or not os.path.exists(local_file):
            return None
        
        # Parse Excel
        wb = openpyxl.load_workbook(local_file, data_only=True)
        
        all_sheets_data = []
        
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            
            # Get headers (first row)
            headers = []
            for cell in ws[1]:
                headers.append(cell.value)
            
            # Get data rows
            sheet_data = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                row_dict = {}
                for idx, value in enumerate(row):
                    if idx < len(headers):
                        # Convert cell values to JSON-serializable types
                        if value is None:
                            row_dict[headers[idx]] = None
                        elif isinstance(value, datetime):
                            row_dict[headers[idx]] = value.isoformat()
                        else:
                            row_dict[headers[idx]] = str(value)
                
                sheet_data.append(row_dict)
            
            all_sheets_data.append({
                'sheet_name': sheet_name,
                'data': sheet_data
            })
        
        # Clean up temp file
        os.remove(local_file)
        
        return all_sheets_data
        
    except Exception as e:
        print(f"Error reading Excel: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_cached_data():
    """
    Get data from cache or refresh if expired
    """
    now = datetime.now()
    
    # Check if cache is valid
    if data_cache['data'] is not None and data_cache['last_updated'] is not None:
        elapsed = (now - data_cache['last_updated']).total_seconds()
        if elapsed < data_cache['cache_duration']:
            return data_cache['data']
    
    # Refresh cache
    print("📥 Refreshing data from Blob Storage...")
    data = read_excel_from_blob()
    
    if data is not None:
        data_cache['data'] = data
        data_cache['last_updated'] = now
        print(f"✅ Cache updated at {now}")
    
    return data

@app.get("/")
def root():
    """API root - health check"""
    return {
        "status": "ok",
        "message": "KATA Testing API is running",
        "version": "1.0.0",
        "endpoints": [
            "/api/degraded-responses",
            "/api/degraded-responses/{sheet_name}",
            "/api/health"
        ]
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache_status": "loaded" if data_cache['data'] is not None else "empty"
    }

@app.get("/api/degraded-responses")
def get_all_degraded_responses():
    """
    Get all degraded responses from all sheets
    
    Returns:
        {
            "total_sheets": 4,
            "total_issues": 15,
            "last_updated": "2026-02-12T10:30:00",
            "sheets": [
                {
                    "sheet_name": "PSP Mentor",
                    "data": [
                        {
                            "Serial Number": "5",
                            "Prompt": "What is DIVE?",
                            "Old Response (Benchmark)": "...",
                            "New Response": "...",
                            "Old Sources": "...",
                            "New Sources": "...",
                            "Benchmark Quality": "GOOD",
                            "Degradation Reason": "Response 60% shorter",
                            "Severity": "HIGH"
                        },
                        ...
                    ]
                },
                ...
            ]
        }
    """
    data = get_cached_data()
    
    if data is None:
        raise HTTPException(status_code=503, detail="Unable to load data from Blob Storage")
    
    total_issues = sum(len(sheet['data']) for sheet in data)
    
    return {
        "total_sheets": len(data),
        "total_issues": total_issues,
        "last_updated": data_cache['last_updated'].isoformat() if data_cache['last_updated'] else None,
        "sheets": data
    }

@app.get("/api/degraded-responses/{sheet_name}")
def get_degraded_responses_by_sheet(sheet_name: str):
    """
    Get degraded responses for a specific sheet
    
    Args:
        sheet_name: One of "PSP Mentor", "VSM Mentor", "TPI Mentor", "Search/Chat"
    
    Returns:
        {
            "sheet_name": "PSP Mentor",
            "total_issues": 5,
            "data": [...]
        }
    """
    data = get_cached_data()
    
    if data is None:
        raise HTTPException(status_code=503, detail="Unable to load data from Blob Storage")
    
    # Find matching sheet (case-insensitive)
    sheet_name_lower = sheet_name.lower()
    for sheet in data:
        if sheet['sheet_name'].lower() == sheet_name_lower:
            return {
                "sheet_name": sheet['sheet_name'],
                "total_issues": len(sheet['data']),
                "data": sheet['data']
            }
    
    raise HTTPException(status_code=404, detail=f"Sheet '{sheet_name}' not found")

@app.post("/api/refresh")
def force_refresh():
    """
    Force refresh data from Blob Storage (manual cache invalidation)
    """
    data_cache['data'] = None
    data_cache['last_updated'] = None
    
    data = get_cached_data()
    
    if data is None:
        raise HTTPException(status_code=503, detail="Unable to refresh data")
    
    return {
        "status": "success",
        "message": "Data refreshed from Blob Storage",
        "total_sheets": len(data),
        "total_issues": sum(len(sheet['data']) for sheet in data)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Part 5: Update Testing Script

Add Blob Storage upload to `integrated_test_comparison.py`:

Add this import at the top:
```python
from blob_storage_uploader import upload_excel_to_blob
```

In the `main()` function, after saving the degraded report, add:
```python
# Upload to Blob Storage
if all_degraded_responses:
    print(f"\n{'='*70}")
    print(f"☁️  Uploading to Azure Blob Storage")
    print(f"{'='*70}")
    blob_url = upload_excel_to_blob(DEGRADED_OUTPUT_FILE)
```

---

## Part 6: Environment Setup

Create `.env` file (NEVER commit this to git!):

```bash
# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=katatestingstorage;AccountKey=YOUR_KEY_HERE;EndpointSuffix=core.windows.net"

# Optional: Teams and SharePoint (keep your existing ones)
TEAMS_WEBHOOK_URL="your-teams-webhook-url"
SHAREPOINT_UPLOAD_URL="your-sharepoint-url"
```

Set environment variable:
```bash
# macOS/Linux
export AZURE_STORAGE_CONNECTION_STRING="your-connection-string"

# Or use python-dotenv to load from .env file
pip install python-dotenv
```

---

## Part 7: Testing Locally

### Test 1: Upload Excel to Blob Storage

```bash
# Make sure you have a degraded responses report
python integrated_test_comparison.py

# Test upload
python blob_storage_uploader.py
```

Expected output:
```
📤 Uploading Degraded_Responses_Report.xlsx to Azure Blob Storage...
✅ Upload successful!
📁 File size: 12,345 bytes
🔗 Blob URL: https://katatestingstorage.blob.core.windows.net/kata-reports/Degraded_Responses_Report.xlsx

✅ Success! File uploaded to: https://...
```

### Test 2: Start FastAPI Server

```bash
python api_server.py
```

Expected output:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test 3: Test API Endpoints

Open another terminal and test:

```bash
# Health check
curl http://localhost:8000/api/health

# Get all degraded responses
curl http://localhost:8000/api/degraded-responses

# Get specific sheet
curl http://localhost:8000/api/degraded-responses/PSP%20Mentor

# Force refresh
curl -X POST http://localhost:8000/api/refresh
```

Or open in browser:
- http://localhost:8000/docs (Interactive API documentation)
- http://localhost:8000/api/degraded-responses

---

## Part 8: Frontend Integration

### React/Next.js Example

```typescript
// api/degradedResponses.ts
interface DegradedResponse {
  "Serial Number": string;
  "Prompt": string;
  "Old Response (Benchmark)": string;
  "New Response": string;
  "Old Sources": string;
  "New Sources": string;
  "Benchmark Quality": string;
  "Degradation Reason": string;
  "Severity": string;
}

interface SheetData {
  sheet_name: string;
  data: DegradedResponse[];
}

interface ApiResponse {
  total_sheets: number;
  total_issues: number;
  last_updated: string;
  sheets: SheetData[];
}

export async function getDegradedResponses(): Promise<ApiResponse> {
  const response = await fetch('http://your-api-url.com/api/degraded-responses');
  
  if (!response.ok) {
    throw new Error('Failed to fetch degraded responses');
  }
  
  return response.json();
}

export async function getDegradedResponsesBySheet(sheetName: string): Promise<SheetData> {
  const response = await fetch(
    `http://your-api-url.com/api/degraded-responses/${encodeURIComponent(sheetName)}`
  );
  
  if (!response.ok) {
    throw new Error(`Failed to fetch data for sheet: ${sheetName}`);
  }
  
  return response.json();
}
```

### React Component Example

```tsx
// components/DegradedResponsesTable.tsx
import { useState, useEffect } from 'react';
import { getDegradedResponses } from '../api/degradedResponses';

export default function DegradedResponsesTable() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const result = await getDegradedResponses();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>No data available</div>;

  return (
    <div>
      <h1>Degraded Responses Report</h1>
      <p>Total Issues: {data.total_issues}</p>
      <p>Last Updated: {new Date(data.last_updated).toLocaleString()}</p>
      
      {data.sheets.map((sheet) => (
        <div key={sheet.sheet_name}>
          <h2>{sheet.sheet_name}</h2>
          <table>
            <thead>
              <tr>
                <th>Serial</th>
                <th>Prompt</th>
                <th>Reason</th>
                <th>Severity</th>
              </tr>
            </thead>
            <tbody>
              {sheet.data.map((row, idx) => (
                <tr key={idx}>
                  <td>{row["Serial Number"]}</td>
                  <td>{row["Prompt"]}</td>
                  <td>{row["Degradation Reason"]}</td>
                  <td>
                    <span className={row.Severity === 'HIGH' ? 'high' : 'medium'}>
                      {row.Severity}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}
```

---

## Part 9: Deployment to Azure

### Option 1: Azure Container Instances (Recommended)

1. **Create Dockerfile**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_server.py .
COPY blob_storage_uploader.py .

EXPOSE 8000

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and push to Azure Container Registry**:

```bash
# Build
docker build -t kata-api .

# Tag and push
az acr login --name yourregistry
docker tag kata-api yourregistry.azurecr.io/kata-api:latest
docker push yourregistry.azurecr.io/kata-api:latest
```

3. **Deploy to Azure Container Instances**:

```bash
az container create \
  --resource-group kata-testing-rg \
  --name kata-api \
  --image yourregistry.azurecr.io/kata-api:latest \
  --dns-name-label kata-api \
  --ports 8000 \
  --environment-variables AZURE_STORAGE_CONNECTION_STRING="your-connection-string"
```

Your API will be available at: `http://kata-api.eastus.azurecontainer.io:8000`

### Option 2: Azure App Service

```bash
# Deploy directly
az webapp up \
  --name kata-api \
  --resource-group kata-testing-rg \
  --runtime PYTHON:3.11 \
  --sku B1

# Set environment variable
az webapp config appsettings set \
  --name kata-api \
  --resource-group kata-testing-rg \
  --settings AZURE_STORAGE_CONNECTION_STRING="your-connection-string"
```

---

## Part 10: GitHub Actions (Automated Deployment)

Update `.github/workflows/daily-kata-test.yml`:

```yaml
name: Daily KATA Test

on:
  schedule:
    - cron: '30 2 * * *'
  workflow_dispatch:

jobs:
  run-kata-test:
    runs-on: ubuntu-latest
    timeout-minutes: 180

    env:
      TZ: 'Asia/Kolkata'
      AZURE_STORAGE_CONNECTION_STRING: ${{ secrets.AZURE_STORAGE_CONNECTION_STRING }}
      TEAMS_WEBHOOK_URL: ${{ secrets.TEAMS_WEBHOOK_URL }}

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run KATA tests and upload to Blob Storage
        run: |
          python integrated_test_comparison.py
```

Set the secret in GitHub:
- Go to: Settings → Secrets and variables → Actions
- Add: `AZURE_STORAGE_CONNECTION_STRING`

---

## Summary

### What You Get:

1. ✅ **Excel uploaded to Blob Storage** (single source of truth)
2. ✅ **FastAPI server** serves data as JSON
3. ✅ **Frontend calls**: `GET /api/degraded-responses`
4. ✅ **Auto-refresh** cache every 5 minutes
5. ✅ **CORS enabled** for frontend access
6. ✅ **Production-ready** deployment options

### API Endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/health` | GET | Detailed health status |
| `/api/degraded-responses` | GET | All degraded responses (all sheets) |
| `/api/degraded-responses/{sheet_name}` | GET | Specific sheet data |
| `/api/refresh` | POST | Force cache refresh |
| `/docs` | GET | Interactive API documentation |

### Next Steps:

1. **Provide me your Azure connection string** → I'll integrate everything
2. **Test locally** following the steps above
3. **Deploy to Azure** using Container Instances or App Service
4. **Share API URL with frontend team**

**Estimated Total Cost:** $10-20/month (Blob Storage + Container Instance)
