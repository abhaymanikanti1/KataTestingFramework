# SharePoint API Setup Guide

## Target Location
**SharePoint Folder:** https://fortive.sharepoint.com/:f:/s/FTV-TheFort/ElR5OWy9Ly1Kh6vX94lw2QEBovoBK7ikri9EDIm08WnhBg?e=ogfAHf
**Site:** https://fortive.sharepoint.com/sites/FTV-TheFort

## Quick Setup: Azure App Registration

### Step 1: Register App in Azure AD
1. Go to https://portal.azure.com
2. Navigate to: **Azure Active Directory** → **App registrations** → **New registration**
3. Fill in:
   - **Name:** `API Quality Monitor` (or any name)
   - **Supported account types:** Accounts in this organizational directory only (Fortive only - Single tenant)
   - **Redirect URI:** Leave blank or use `http://localhost`
4. Click **Register**

### Step 2: Copy App Credentials
After registration, on the **Overview** page, copy:
- ✅ **Application (client) ID:** `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- ✅ **Directory (tenant) ID:** `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

### Step 3: Create Client Secret
1. Go to **Certificates & secrets** (left sidebar)
2. Click **New client secret**
3. Description: `API Quality Upload Secret`
4. Expires: Choose duration (recommend 12-24 months)
5. Click **Add**
6. ⚠️ **COPY THE SECRET VALUE IMMEDIATELY** (shown only once!)
   - ✅ **Client Secret:** `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 4: Grant SharePoint Permissions
1. Go to **API permissions** (left sidebar)
2. Click **Add a permission** → **SharePoint**
3. Choose **Application permissions** (for unattended automation)
4. Select: `Sites.ReadWrite.All`
5. Click **Add permissions**
6. Click **Grant admin consent for Fortive** (requires admin rights)
   - ⚠️ If you don't have admin rights, ask your IT admin to grant consent

### Step 5: Share Credentials with Developer

Please provide these 4 values:

```
CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SHAREPOINT_SITE_URL=https://fortive.sharepoint.com/sites/FTV-TheFort
```

---

## Alternative: If You Don't Have Azure AD Admin Access

If you cannot create an Azure App Registration, we can use one of these alternatives:

### Option A: Personal Access Token (Simpler but less secure)
- Not recommended for production automation
- Would require your credentials stored in code

### Option B: Ask IT Admin
- Request your IT admin to create the App Registration
- They can share the Client ID, Tenant ID, and Client Secret with you

### Option C: Use Power Automate
- Create a Power Automate flow that:
  1. Receives HTTP webhook with file content (base64 encoded)
  2. Uploads to SharePoint
  3. Returns the file URL
- More complex but doesn't require App Registration

---

## What Happens Next?

Once you provide the credentials:
1. ✅ I'll install the `msal` library for authentication
2. ✅ I'll create an `upload_to_sharepoint()` function
3. ✅ I'll integrate it into `integrated_test_comparison.py`
4. ✅ I'll update the Teams alert to include the SharePoint file link
5. ✅ I'll test the upload with a sample file
6. ✅ We'll add credentials to GitHub Actions secrets for automation

---

## Security Note
⚠️ Never commit credentials directly to code or GitHub!
✅ Use environment variables or GitHub Secrets
✅ Client secrets should be rotated periodically
