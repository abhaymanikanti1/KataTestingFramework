# Fix Azure App Service - Environment Variable Missing

## Problem
Azure App Service is running but returns error:
```json
{"detail":"Unable to load data from Blob Storage. Check if the Excel file exists and the connection string is configured."}
```

This means the `AZURE_STORAGE_CONNECTION_STRING` environment variable is not set.

## Solution: Set Environment Variable in Azure Portal

### Step 1: Access Azure Portal
1. Go to https://portal.azure.com
2. Sign in with your credentials

### Step 2: Navigate to App Service
1. Click **Resource groups** (left sidebar)
2. Click **rg-kata-v2**
3. Click **kata-api-v2** (App Service)

### Step 3: Add Environment Variable
1. In the left menu, click **Configuration** (under Settings)
2. Click the **Application settings** tab
3. Click **+ New application setting**
4. Fill in:
   - **Name:** `AZURE_STORAGE_CONNECTION_STRING`
   - **Value:** (see below)

### Step 4: Connection String Value
**⚠️ Get your connection string from:**
1. Azure Portal → Storage Account `katauploads` → Access Keys
2. Copy the entire **Connection string** from Key1 or Key2
3. Paste it as the value for `AZURE_STORAGE_CONNECTION_STRING`

### Step 5: Save
1. Click **OK** (on the new application setting dialog)
2. Click **Save** (at the top of the Configuration page)
3. Click **Continue** when prompted about restarting the app

### Step 6: Test
Wait 30-60 seconds for the restart, then test:

```bash
curl https://kata-api-v2.azurewebsites.net/api/health
```

You should see:
```json
{
  "status": "healthy",
  "blob_storage": {
    "connected": true,
    "blob_exists": true
  }
}
```

---

## Alternative: Use Azure CLI

If you prefer command line:

```bash
az webapp config appsettings set \
  --resource-group rg-kata-v2 \
  --name kata-api-v2 \
  --settings AZURE_STORAGE_CONNECTION_STRING="<YOUR_CONNECTION_STRING_FROM_AZURE_PORTAL>"

# Restart the app
az webapp restart --resource-group rg-kata-v2 --name kata-api-v2

# Wait 30 seconds then test
sleep 30
curl https://kata-api-v2.azurewebsites.net/api/health
```

---

## Verification Checklist

After setting the environment variable:

- [ ] Environment variable saved in Configuration
- [ ] App Service restarted
- [ ] Health endpoint responds: `https://kata-api-v2.azurewebsites.net/api/health`
- [ ] Blob storage shows connected: `"blob_storage": {"connected": true}`
- [ ] Data endpoint works: `https://kata-api-v2.azurewebsites.net/api/degraded-responses`

---

## If Still Not Working

Check App Service logs:
```bash
az webapp log tail --name kata-api-v2 --resource-group rg-kata-v2
```

Or in Azure Portal:
1. Go to kata-api-v2
2. Click **Log stream** (under Monitoring)
3. Watch for errors

---

## Local API (Works Now)

While fixing Azure, your local API is fully functional:

```
http://localhost:8000
```

Your frontend team can use this immediately if they're on the same network.
