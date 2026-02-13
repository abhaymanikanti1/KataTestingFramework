# Quick Start Guide - Setup in 10 Minutes

## What You'll Build

```
Testing Script → Azure Blob Storage → FastAPI Server → Frontend (JSON)
```

Your frontend will call: `GET http://your-api.com/api/degraded-responses` and get clean JSON data.

---

## Step 1: Azure Setup (3 minutes)

### 1.1 Create Storage Account

```bash
# Login to Azure
az login

# Create resource group
az group create --name kata-testing-rg --location eastus

# Create storage account (replace 'uniquename' with something unique)
az storage account create \
  --name katatestinguniquename \
  --resource-group kata-testing-rg \
  --location eastus \
  --sku Standard_LRS

# Create container
az storage container create \
  --name kata-reports \
  --account-name katatestinguniquename
```

### 1.2 Get Connection String

```bash
az storage account show-connection-string \
  --name katatestinguniquename \
  --resource-group kata-testing-rg \
  --output tsv
```

**Copy the output** - it looks like:
```
DefaultEndpointsProtocol=https;AccountName=katatestinguniquename;AccountKey=xxxxx;EndpointSuffix=core.windows.net
```

---

## Step 2: Local Setup (2 minutes)

### 2.1 Install Dependencies

```bash
cd /Users/abhay.manikanti/Downloads/KataTestingFramework-main

# Install Python packages
pip install -r requirements.txt
```

### 2.2 Set Environment Variable

```bash
# macOS/Linux
export AZURE_STORAGE_CONNECTION_STRING="paste-your-connection-string-here"

# Verify it's set
echo $AZURE_STORAGE_CONNECTION_STRING
```

---

## Step 3: Test Upload (1 minute)

```bash
# Run the testing script to generate the Excel file and upload it
python integrated_test_comparison.py
```

You should see:
```
☁️  Uploading to Azure Blob Storage
📤 Uploading Degraded_Responses_Report.xlsx to Azure Blob Storage...
✅ Upload successful!
📁 File size: 12,345 bytes
🔗 Blob URL: https://katatestinguniquename.blob.core.windows.net/kata-reports/Degraded_Responses_Report.xlsx
```

✅ **If you see this, the upload works!**

---

## Step 4: Start API Server (1 minute)

```bash
# Start the FastAPI server
python api_server.py
```

You should see:
```
🚀 Starting KATA Testing API Server
📡 Server: http://0.0.0.0:8000
📚 API Docs: http://0.0.0.0:8000/docs
```

---

## Step 5: Test API Endpoints (1 minute)

Open your browser and test these URLs:

### 5.1 Interactive API Docs
```
http://localhost:8000/docs
```
This gives you a Swagger UI to test all endpoints.

### 5.2 Get All Data
```
http://localhost:8000/api/degraded-responses
```

You should see JSON like:
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
          "Old Response (Benchmark)": "...",
          "New Response": "...",
          "Severity": "HIGH"
        }
      ]
    }
  ]
}
```

### 5.3 Get Specific Sheet
```
http://localhost:8000/api/degraded-responses/PSP%20Mentor
```

### 5.4 Health Check
```
http://localhost:8000/api/health
```

---

## Step 6: Frontend Integration (2 minutes)

Tell your frontend team to call:

```typescript
// Simple fetch example
const response = await fetch('http://your-api-url/api/degraded-responses');
const data = await response.json();

console.log(data.total_issues);  // Number of issues
console.log(data.sheets);         // Array of sheet data
```

Full examples in: `frontend_examples.py`

---

## Step 7: Deploy to Production (Optional)

### Option A: Docker (Recommended)

```bash
# Build image
docker build -t kata-api .

# Run locally
docker run -p 8000:8000 \
  -e AZURE_STORAGE_CONNECTION_STRING="your-connection-string" \
  kata-api

# Test
curl http://localhost:8000/api/health
```

### Option B: Azure Container Instances

```bash
# Create container instance
az container create \
  --resource-group kata-testing-rg \
  --name kata-api \
  --image your-registry.azurecr.io/kata-api:latest \
  --dns-name-label kata-api-prod \
  --ports 8000 \
  --environment-variables \
    AZURE_STORAGE_CONNECTION_STRING="your-connection-string"

# Get URL
az container show \
  --resource-group kata-testing-rg \
  --name kata-api \
  --query ipAddress.fqdn \
  --output tsv
```

Your API will be at: `http://kata-api-prod.eastus.azurecontainer.io:8000`

### Option C: Azure App Service

```bash
# Create and deploy
az webapp up \
  --name kata-api-prod \
  --resource-group kata-testing-rg \
  --runtime PYTHON:3.11 \
  --sku B1

# Set environment variable
az webapp config appsettings set \
  --name kata-api-prod \
  --resource-group kata-testing-rg \
  --settings AZURE_STORAGE_CONNECTION_STRING="your-connection-string"
```

Your API will be at: `https://kata-api-prod.azurewebsites.net`

---

## Step 8: Update GitHub Actions

Add to your repository secrets (Settings → Secrets → Actions):

```
Name: AZURE_STORAGE_CONNECTION_STRING
Value: Your connection string
```

The workflow is already configured to upload to Blob Storage automatically!

---

## Troubleshooting

### "AZURE_STORAGE_CONNECTION_STRING not set"

```bash
# Check if it's set
echo $AZURE_STORAGE_CONNECTION_STRING

# If empty, set it again
export AZURE_STORAGE_CONNECTION_STRING="your-connection-string"
```

### "Unable to load data from Blob Storage"

```bash
# Check if file exists
python -c "from blob_storage_uploader import check_blob_exists; print(check_blob_exists())"

# If False, upload the file first
python integrated_test_comparison.py
```

### API returns 503 error

The Excel file doesn't exist in Blob Storage yet. Run:
```bash
python integrated_test_comparison.py
```

### CORS errors from frontend

Update `api_server.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],  # Specify your domain
    ...
)
```

---

## What to Share with Frontend Team

1. **API Base URL**: 
   - Local: `http://localhost:8000`
   - Production: `http://your-deployed-url`

2. **Main Endpoint**: 
   ```
   GET /api/degraded-responses
   ```

3. **Response Format**:
   ```json
   {
     "total_sheets": number,
     "total_issues": number,
     "last_updated": "ISO date string",
     "sheets": [
       {
         "sheet_name": string,
         "row_count": number,
         "data": [
           {
             "Serial Number": string,
             "Prompt": string,
             "Old Response (Benchmark)": string,
             "New Response": string,
             "Severity": "HIGH" | "MEDIUM",
             ...
           }
         ]
       }
     ]
   }
   ```

4. **API Documentation**: 
   ```
   http://your-api-url/docs
   ```

5. **Frontend Examples**: 
   See `frontend_examples.py` for React/Vue/TypeScript code

---

## Cost Estimate

- **Blob Storage**: $0.02/month (for 1GB)
- **Azure Container Instance**: $10-20/month
- **Azure App Service (B1)**: $13/month

**Total: ~$15-20/month**

---

## Next Steps

1. ✅ Get Azure connection string from portal
2. ✅ Run `pip install -r requirements.txt`
3. ✅ Set `AZURE_STORAGE_CONNECTION_STRING` environment variable
4. ✅ Run `python integrated_test_comparison.py` to test upload
5. ✅ Run `python api_server.py` to start API
6. ✅ Test at `http://localhost:8000/docs`
7. ✅ Share API URL with frontend team
8. ✅ Deploy to Azure (optional but recommended)

**You're ready to go! 🚀**
