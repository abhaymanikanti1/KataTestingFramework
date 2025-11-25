# Add SharePoint Upload Action - Step by Step

## Current Status: ✅ HTTP Trigger Works!
Your flow successfully returns: `{"message":"Flow triggered successfully","received":true}`

## Now Add SharePoint Upload

### Step 1: Add SharePoint Action

1. In your flow, click **"+ New step"** (between HTTP trigger and Response)
2. Search for: **"SharePoint"**
3. Choose: **"Create file"**

---

### Step 2: Configure SharePoint Connection

If prompted to sign in:
- Sign in with your Fortive credentials
- Allow the connection

---

### Step 3: Configure Site Address

**Site Address:**
- Click the dropdown
- Look for: `https://fortive.sharepoint.com/sites/FTV-TheFort`
- If not in list: Click "Enter custom value" and paste the URL

---

### Step 4: Configure Folder Path

**IMPORTANT:** The folder must already exist in SharePoint!

**Option A: Browse (Recommended)**
- Click the 📁 folder icon
- Navigate to your target folder
- Select it

**Option B: Manual Entry**
- Type the path starting with `/`
- Examples:
  - `/Shared Documents`
  - `/Shared Documents/API Reports`
  - `/Documents/Reports`

**To find the correct path:**
1. Go to your SharePoint folder: https://fortive.sharepoint.com/:f:/s/FTV-TheFort/ElR5OWy9Ly1Kh6vX94lw2QEBovoBK7ikri9EDIm08WnhBg
2. Look at the folder structure
3. Use the path from "Shared Documents" or "Documents" onward

---

### Step 5: Configure File Name

**File Name:**
1. Click in the "File Name" field
2. A panel opens on the right
3. Click **"Dynamic content"** tab
4. Under "When a HTTP request is received"
5. Click **"filename"**
6. Result: `@{triggerBody()?['filename']}`

This is correct - the `?` is fine here.

---

### Step 6: Configure File Content (CRITICAL!)

**File Content:**
1. Click in the "File Content" field
2. A panel opens on the right
3. Click **"Expression"** tab (NOT Dynamic content!)
4. Type EXACTLY:
   ```
   base64ToBinary(triggerBody()['fileContent'])
   ```
5. Click **"OK"**
6. Verify it shows: `@{base64ToBinary(triggerBody()['fileContent'])}`

**⚠️ CRITICAL:**
- Use **Expression** tab, NOT Dynamic content
- NO `?` before the brackets: `triggerBody()['fileContent']` ✅
- NOT: `triggerBody()?['fileContent']` ❌

---

### Step 7: Update Response Action

Update your Response action to return the SharePoint file URL:

1. Click on the **"Response"** action
2. Change the Body to:
```json
{
  "success": true,
  "fileUrl": "@{outputs('Create_file')?['body/{Link}']}"
}
```

**Note:** If your SharePoint action has a different name, replace `'Create_file'` with the actual name (shown in the action's title bar).

---

### Step 8: Save and Test

1. Click **"Save"** in the top right
2. Wait for "Your flow is ready"
3. Run the test:
   ```bash
   python test_flow_simple.py
   ```

**Expected result:**
```
Status: 200
Response: {"success":true,"fileUrl":"https://fortive.sharepoint.com/..."}
```

---

## Troubleshooting

### If you get "Folder not found"
- The folder path doesn't exist in SharePoint
- Go create the folder first, then try again

### If you still get base64ToBinary Null error
- You used `?` in the expression
- Delete the File Content field and re-enter using Expression tab
- Make sure it's: `base64ToBinary(triggerBody()['fileContent'])` with NO `?`

### If you get "Access denied"
- The flow doesn't have permission to that SharePoint site/folder
- Try uploading to `/Shared Documents` directly first
- Or ask IT to grant access to the specific folder

### If test still shows 500
- Check Run History in Power Automate
- Look for the specific error on the SharePoint action
- The tracking ID will help identify the exact issue
