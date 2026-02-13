# 🎯 What I Need from You to Complete the Setup

## Just ONE Thing: Azure Storage Connection String

### How to Get It

#### Option 1: Azure Portal (GUI)

1. Go to: https://portal.azure.com
2. Search for **"Storage accounts"**
3. If you have one already:
   - Click on it → **Access keys** (left menu) → **Show keys** → Copy **Connection string** under key1
4. If you don't have one:
   - Click **+ Create**
   - Fill in:
     - **Resource Group**: Create new `kata-testing-rg`
     - **Storage account name**: `katatesting<yourname>` (must be unique, lowercase, no spaces)
     - **Region**: `East US`
     - **Performance**: `Standard`
     - **Redundancy**: `LRS`
   - Click **Review + Create** → **Create**
   - Wait ~1 minute
   - Go to the storage account → **Containers** → **+ Container**
   - Name: `kata-reports`
   - Public access: `Private`
   - Click **Create**
   - Go back to **Access keys** → Copy **Connection string**

#### Option 2: Azure CLI (Command Line)

```bash
# Login
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

# Get connection string
az storage account show-connection-string \
  --name katatestinguniquename \
  --resource-group kata-testing-rg \
  --output tsv
```

### What It Looks Like

```
DefaultEndpointsProtocol=https;AccountName=katatestinguniquename;AccountKey=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;EndpointSuffix=core.windows.net
```

### Send Me This

Just copy-paste the entire connection string above.

---

## What I'll Do Once You Give Me the Connection String

### 1. Test the Upload (1 minute)

```bash
export AZURE_STORAGE_CONNECTION_STRING="your-connection-string"
python integrated_test_comparison.py
```

**Expected output:**
```
☁️  Uploading to Azure Blob Storage
📤 Uploading Degraded_Responses_Report.xlsx to Azure Blob Storage...
✅ Upload successful!
📁 File size: 12,345 bytes
🔗 Blob URL: https://...
```

### 2. Start the API Server (1 minute)

```bash
python api_server.py
```

**Expected output:**
```
🚀 Starting KATA Testing API Server
📡 Server: http://0.0.0.0:8000
📚 API Docs: http://0.0.0.0:8000/docs
```

### 3. Verify API Works (1 minute)

Visit: http://localhost:8000/docs

Test endpoint: `GET /api/degraded-responses`

**Expected response:**
```json
{
  "total_sheets": 4,
  "total_issues": 15,
  "last_updated": "2026-02-12T10:30:00",
  "sheets": [...]
}
```

### 4. Share with Frontend Team (immediate)

Give them:
- **API URL** (after deployment)
- **Endpoint**: `GET /api/degraded-responses`
- **Example code** from `frontend_examples.py`
- **API Docs URL**: `http://your-api-url/docs`

---

## Frontend Team Can Start Immediately

They don't need to wait! They can:

1. **Mock the API response** using the example JSON in `FRONTEND_API_SETUP_GUIDE.md`

2. **Use TypeScript interfaces** from `frontend_examples.py`:
   ```typescript
   interface DegradedResponse {
     "Serial Number": string;
     "Prompt": string;
     "Severity": "HIGH" | "MEDIUM";
     // ... etc
   }
   ```

3. **Build the UI/table** with mock data

4. **Switch to real API** once we deploy (just change the URL)

---

## Deployment Options (After Local Testing Works)

### Option A: Azure Container Instances (~$15/month)

I'll run:
```bash
docker build -t kata-api .
az acr create --name yourregistry --resource-group kata-testing-rg --sku Basic
az acr login --name yourregistry
docker tag kata-api yourregistry.azurecr.io/kata-api:latest
docker push yourregistry.azurecr.io/kata-api:latest

az container create \
  --name kata-api \
  --resource-group kata-testing-rg \
  --image yourregistry.azurecr.io/kata-api:latest \
  --dns-name-label kata-api-prod \
  --ports 8000 \
  --environment-variables AZURE_STORAGE_CONNECTION_STRING="your-string"
```

**Your API URL:** `http://kata-api-prod.eastus.azurecontainer.io:8000`

### Option B: Azure App Service (~$13/month)

I'll run:
```bash
az webapp up \
  --name kata-api-prod \
  --resource-group kata-testing-rg \
  --runtime PYTHON:3.11 \
  --sku B1

az webapp config appsettings set \
  --name kata-api-prod \
  --resource-group kata-testing-rg \
  --settings AZURE_STORAGE_CONNECTION_STRING="your-string"
```

**Your API URL:** `https://kata-api-prod.azurewebsites.net`

---

## Timeline

Once you give me the connection string:

- **5 minutes:** Test upload & API locally
- **10 minutes:** Deploy to Azure
- **2 minutes:** Share API URL with frontend team

**Total: ~20 minutes and you're live! 🚀**

---

## What Frontend Gets

### Simple API Call
```typescript
const response = await fetch('http://your-api-url/api/degraded-responses');
const data = await response.json();
```

### Clean JSON Response
```json
{
  "total_sheets": 4,
  "total_issues": 15,
  "sheets": [
    {
      "sheet_name": "PSP Mentor",
      "row_count": 5,
      "data": [
        {
          "Serial Number": "5",
          "Prompt": "What is DIVE?",
          "Old Response (Benchmark)": "Detailed...",
          "New Response": "Short...",
          "Severity": "HIGH",
          "Degradation Reason": "Response 60% shorter"
        }
      ]
    }
  ]
}
```

All fields from Excel, formatted as JSON, ready to display in a table.

---

## Cost Breakdown

| Item | Cost |
|------|------|
| Blob Storage (1GB) | $0.02/month |
| Container Instance (1 vCPU, 1.5GB) | $15/month |
| OR App Service (B1) | $13/month |

**Total: ~$13-15/month**

---

## Summary

**You provide:** Azure Storage Connection String (one line of text)

**You get:**
- ✅ Excel auto-uploads to Blob Storage
- ✅ FastAPI serves data as JSON
- ✅ Frontend gets clean API endpoint
- ✅ Interactive API docs
- ✅ Production deployment
- ✅ Auto-updates daily

**All in ~20 minutes!**

---

## Next Step

**Send me the Azure Storage Connection String and I'll complete the setup!**

Format:
```
DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net
```
