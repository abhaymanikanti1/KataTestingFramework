# GitHub Actions Setup Guide

## Overview

This repository includes automated testing workflows that:
- Run daily at 9 AM UTC
- Test API responses against benchmarks
- Upload results to Azure Blob Storage
- Send alerts to Microsoft Teams
- Deploy data to kata-api-v2 for frontend access

---

## 🚀 Quick Setup

### Step 1: Push Code to GitHub

```bash
cd /Users/abhay.manikanti/Downloads/KataTestingFramework-main

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: KATA Testing Framework with API"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

---

## 🔐 Step 2: Configure GitHub Secrets

Go to your GitHub repository:
1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add each of the following secrets:

### Required Secrets

#### Azure Blob Storage
**Name:** `AZURE_STORAGE_CONNECTION_STRING`  
**Value:** Get from Azure Portal → Storage Account `katauploads` → Access Keys → Connection string

#### API Configuration
**Name:** `API_BASE_URL`  
**Value:** `https://container-app-ui-stage.purplesky-e0183d2f.eastus.azurecontainerapps.io/`

**Name:** `EMAIL_ID`  
**Value:** `abhay.manikanti@fortive.com`

**Name:** `API_KEY`  
**Value:** `d7e8f9b6-92a4-48e2-a0cd-f81c993f29c1`

**Name:** `SESSION_ID`  
**Value:** `43908e3d-7fee-4688-a6c5-f3bd32a94ffd`

#### Microsoft Teams
**Name:** `TEAMS_WEBHOOK_URL`  
**Value:** (Your Teams webhook URL - find in teams_webhook_setup_instructions.txt)

#### SharePoint (Optional - if using SharePoint integration)
**Name:** `SHAREPOINT_SITE_URL`  
**Value:** (Your SharePoint site URL)

**Name:** `SHAREPOINT_CLIENT_ID`  
**Value:** (Your SharePoint app client ID)

**Name:** `SHAREPOINT_CLIENT_SECRET`  
**Value:** (Your SharePoint app secret)

---

## 📅 Step 3: Workflow Schedule

The workflow runs automatically:
- **Daily:** 9 AM UTC (4 AM EST / 1 AM PST)
- **Manual:** Click "Actions" → "Daily API Testing & Deployment" → "Run workflow"

### Adjust Schedule

Edit `.github/workflows/daily-api-testing.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Change time here (format: minute hour day month dayofweek)
```

Examples:
- `0 14 * * *` - 2 PM UTC daily
- `0 9 * * 1-5` - 9 AM UTC Monday-Friday
- `0 0 * * 0` - Midnight UTC every Sunday

---

## ✅ Step 4: Test the Workflow

### Option 1: Wait for scheduled run
The workflow will run automatically at the scheduled time.

### Option 2: Manual trigger
1. Go to GitHub repository
2. Click **Actions** tab
3. Click **Daily API Testing & Deployment**
4. Click **Run workflow** dropdown
5. Click **Run workflow** button

---

## 📊 Step 5: View Results

### In GitHub Actions
1. Go to **Actions** tab
2. Click on the latest workflow run
3. View logs and download artifacts

### In Azure Blob Storage
Results are automatically uploaded to:
- Storage Account: `katauploads`
- Container: `kata-reports`
- File: `degraded_responses.xlsx`

### Via API
Frontend team can access results via:
```
GET https://kata-api-v2.azurewebsites.net/api/degraded-responses
```

### In Microsoft Teams
Alerts are sent to the configured Teams channel when degraded responses are detected.

---

## 🔄 Workflow Details

### What Happens During Each Run

1. **Setup Environment**
   - Checkout latest code
   - Install Python 3.11
   - Install dependencies from requirements.txt

2. **Run Tests**
   - Execute `integrated_test_comparison.py`
   - Test API responses against benchmarks
   - Generate degraded responses report

3. **Upload Results**
   - Upload to Azure Blob Storage (`degraded_responses.xlsx`)
   - Send Teams alert if degraded responses found
   - Save as GitHub artifact (kept for 30 days)

4. **Notifications**
   - Success: Summary in workflow logs
   - Failure: GitHub sends email to repository watchers

---

## 📁 Artifacts

GitHub Actions saves test results as artifacts:
- **Retention:** 30 days
- **Location:** Actions → Workflow run → Artifacts section
- **Files included:**
  - `Degraded_Responses_Report.xlsx`
  - `Direct Query Master List V_Test.xlsx`

---

## 🔍 Monitoring & Debugging

### View Workflow Logs
1. Go to **Actions** tab
2. Click on workflow run
3. Click on job name
4. Expand steps to view detailed logs

### Common Issues

#### Workflow not running
- Check the cron schedule is correct
- Ensure repository is not archived
- Verify Actions are enabled in repository settings

#### Secrets not found
- Double-check secret names match exactly (case-sensitive)
- Verify secrets are set at repository level, not environment level

#### Tests failing
- Check API_BASE_URL is accessible
- Verify API_KEY and credentials are valid
- Review workflow logs for specific error messages

#### Upload to Blob Storage fails
- Verify AZURE_STORAGE_CONNECTION_STRING is correct
- Check Azure storage account is accessible
- Ensure container `kata-reports` exists

---

## 🛠️ Maintenance

### Update Dependencies
Edit `requirements.txt` and push changes. Next workflow run will use updated versions.

### Modify Test Configuration
Edit `integrated_test_comparison.py`:
- Change `TEST_LIMIT` for number of rows to test
- Update `API_BASE_URL` if backend changes
- Modify sheet configurations in `SHEET_CONFIGS`

### Change Workflow Trigger
Edit `.github/workflows/daily-api-testing.yml`:
- Modify `cron` schedule
- Add additional triggers (e.g., on pull request)

---

## 📧 Notifications

### Email Notifications
GitHub automatically sends emails for:
- Workflow failures (to repository watchers)
- First workflow success after failure

To configure:
1. Go to GitHub profile → Settings → Notifications
2. Enable "Actions" notifications

### Teams Notifications
Configured via `TEAMS_WEBHOOK_URL` secret. Sends:
- Number of degraded responses found
- Link to detailed report
- Timestamp of test run

---

## 🔐 Security Best Practices

✅ **DO:**
- Store all credentials in GitHub Secrets
- Rotate API keys regularly
- Review workflow logs for sensitive data before sharing
- Use least-privilege access for service accounts

❌ **DON'T:**
- Commit `.env` files to repository
- Share secrets in pull request comments
- Log sensitive data in workflow steps
- Use personal credentials for automation

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Cron Schedule](https://crontab.guru/)

---

## ✅ Checklist

Before going live:

- [ ] Code pushed to GitHub repository
- [ ] All secrets configured in repo settings
- [ ] `.gitignore` includes sensitive files
- [ ] Workflow runs successfully (manual trigger test)
- [ ] Results appear in Azure Blob Storage
- [ ] Teams alerts working
- [ ] Frontend team can access API data
- [ ] Team notified of automation schedule

---

**Last Updated:** February 13, 2026  
**Maintained By:** KATA Testing Team
