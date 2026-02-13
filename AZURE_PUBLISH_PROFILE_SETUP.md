# Azure Publish Profile Setup for GitHub Actions

## Overview
The GitHub Actions workflows deploy the API to Azure App Service after running tests. This requires the Azure publish profile secret.

## Get Publish Profile from Azure

### Method 1: Azure Portal (Recommended)
1. Go to https://portal.azure.com
2. Navigate to **Resource Groups** → **rg-kata-v2** → **kata-api-v2**
3. Click **Get publish profile** button (top toolbar)
4. Save the downloaded `.PublishSettings` file
5. Open the file and copy the entire XML content

### Method 2: Azure CLI
```bash
az webapp deployment list-publishing-profiles \
  --name kata-api-v2 \
  --resource-group rg-kata-v2 \
  --xml
```

## Add Secret to GitHub

1. Go to: https://github.com/abhaymanikanti1/KataTestingFramework/settings/secrets/actions
2. Click **New repository secret**
3. Add the secret:
   - **Name:** `AZURE_WEBAPP_PUBLISH_PROFILE`
   - **Value:** Paste the entire XML content from the publish profile

## Required GitHub Secrets Summary

After adding the publish profile, you'll need these 7 secrets total:

1. ✅ `AZURE_WEBAPP_PUBLISH_PROFILE` - Azure App Service deployment credentials
2. `AZURE_STORAGE_CONNECTION_STRING` - Blob storage connection
3. `API_BASE_URL` - Base URL for API testing  
4. `EMAIL_ID` - Login email for testing
5. `API_KEY` - API authentication key
6. `SESSION_ID` - Session identifier
7. `TEAMS_WEBHOOK_URL` - Teams notifications webhook

## Workflow Deployment Steps

The workflows now include:
1. **Run Tests** - Execute `integrated_test_comparison.py`
2. **Upload to Blob** - Save results to Azure Storage
3. **Send Teams Alert** - Notify via webhook
4. **Deploy API** - Deploy latest code to Azure App Service
5. **Verify** - Health check the deployed API

## Testing the Deployment

After configuring the secret:

### Trigger Manual Workflow
1. Go to: https://github.com/abhaymanikanti1/KataTestingFramework/actions
2. Select **Manual API Testing** workflow
3. Click **Run workflow**
4. Wait for completion (~3-5 minutes)

### Check Results
- GitHub Actions logs will show deployment progress
- API should be available at: https://kata-api-v2.azurewebsites.net
- Health check: https://kata-api-v2.azurewebsites.net/api/health
- Data endpoint: https://kata-api-v2.azurewebsites.net/api/degraded-responses

## Troubleshooting

### Deployment Fails
- Verify the publish profile secret is correct (entire XML content)
- Check Azure App Service is running: `az webapp show --name kata-api-v2 --resource-group rg-kata-v2`
- Review workflow logs for specific errors

### API Not Responding After Deployment
- Wait 30-60 seconds for cold start
- Check environment variables are set in Azure Portal
- View App Service logs: `az webapp log tail --name kata-api-v2 --resource-group rg-kata-v2`

---

## What Gets Deployed

The workflow deploys these files to Azure App Service:
- `api_server.py` - FastAPI application
- `blob_storage_uploader.py` - Azure storage client
- `requirements.txt` - Python dependencies
- All supporting modules and configuration

The deployment ensures the frontend team always has access to the latest test results via the API.
