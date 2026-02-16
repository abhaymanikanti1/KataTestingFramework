# 🔐 GitHub Secrets Configuration Guide

## Quick Setup - 7 Required Secrets

Go to: **https://github.com/abhaymanikanti1/KataTestingFramework/settings/secrets/actions**

---

## 1. AZURE_WEBAPP_PUBLISH_PROFILE

**What it does:** Deploys API to Azure App Service after testing

**How to get it:**
```bash
# Already downloaded to: azure_publish_profile.xml
cat azure_publish_profile.xml
```

Copy the entire XML content and paste as the secret value.

---

## 2. AZURE_STORAGE_CONNECTION_STRING

**What it does:** Uploads test results to Azure Blob Storage

**How to get it:**
```bash
az storage account show-connection-string \
  --name katauploads \
  --resource-group rg-kata-v2 \
  --output tsv
```

Or from Azure Portal:
- Storage Account `katauploads` → Access Keys → Connection string

---

## 3. API_BASE_URL

**What it does:** Base URL for API testing

**Value:** Your API endpoint (example: `https://api.example.com`)

---

## 4. EMAIL_ID

**What it does:** Login email for API authentication

**Value:** Your test account email address

---

## 5. API_KEY

**What it does:** API authentication key

**Value:** Your API key for authentication

---

## 6. SESSION_ID

**What it does:** Session identifier for API calls

**Value:** Your session ID

---

## 7. TEAMS_WEBHOOK_URL

**What it does:** Sends notifications to Microsoft Teams

**Value:** Your Teams webhook URL

**How to get it:**
1. Teams → Channel → Connectors → Incoming Webhook
2. Configure and copy the webhook URL

---

## Adding Secrets to GitHub

For each secret above:

1. Go to: https://github.com/abhaymanikanti1/KataTestingFramework/settings/secrets/actions
2. Click **"New repository secret"**
3. Enter the **Name** (exactly as shown above, e.g., `AZURE_WEBAPP_PUBLISH_PROFILE`)
4. Paste the **Value**
5. Click **"Add secret"**

---

## Test the Workflow

After adding all secrets:

1. Go to: https://github.com/abhaymanikanti1/KataTestingFramework/actions
2. Select **"Manual API Testing"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Watch the progress (takes ~3-5 minutes)

The workflow will:
1. ✅ Run API tests
2. ✅ Upload results to Azure Blob Storage  
3. ✅ Send Teams notification
4. ✅ Deploy API to kata-api-v2.azurewebsites.net
5. ✅ Verify deployment with health check

---

## What Happens Daily

At **9 AM UTC every day**, GitHub Actions automatically:

1. Runs all API tests  
2. Generates `Degraded_Responses_Report.xlsx`
3. Uploads report to Azure Blob Storage (`kata-reports/degraded_responses.xlsx`)
4. Sends alert to Microsoft Teams
5. Deploys latest API code to Azure App Service
6. Makes data available at: **https://kata-api-v2.azurewebsites.net/api/degraded-responses**

Your frontend team can fetch the latest results anytime from the API URL!

---

## Verification Checklist

- [ ] All 7 secrets added to GitHub
- [ ] Manual workflow test successful
- [ ] API deployed: https://kata-api-v2.azurewebsites.net/api/health
- [ ] Data endpoint working: https://kata-api-v2.azurewebsites.net/api/degraded-responses
- [ ] Teams notification received
- [ ] Daily workflow scheduled (check Actions tab)

---

## Quick Reference

| Secret Name | Purpose |
|-------------|---------|
| `AZURE_WEBAPP_PUBLISH_PROFILE` | Deploy API to Azure |
| `AZURE_STORAGE_CONNECTION_STRING` | Upload test results |
| `API_BASE_URL` | API endpoint for testing |
| `EMAIL_ID` | Login credentials |
| `API_KEY` | Authentication |
| `SESSION_ID` | Session management |
| `TEAMS_WEBHOOK_URL` | Notifications |

---

## Need Help?

- Workflow logs: https://github.com/abhaymanikanti1/KataTestingFramework/actions
- Azure Portal: https://portal.azure.com
- App Service logs: `az webapp log tail --name kata-api-v2 --resource-group rg-kata-v2`
