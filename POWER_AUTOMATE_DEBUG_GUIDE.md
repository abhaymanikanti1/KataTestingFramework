# Power Automate Flow Debugging Guide

## Current Issue
The flow is returning HTTP 500 (Internal Server Error) for all requests.
This means there's a configuration problem in the flow itself.

## Flow Configuration Checklist

### 1. HTTP Trigger Configuration
Go to https://make.powerautomate.com → Your flow → Edit

**HTTP Trigger Settings:**
- Click on the trigger "When a HTTP request is received"
- Make sure the Request Body JSON Schema is set to:

```json
{
    "type": "object",
    "properties": {
        "filename": {
            "type": "string"
        },
        "fileContent": {
            "type": "string"
        },
        "timestamp": {
            "type": "string"
        }
    }
}
```

### 2. SharePoint "Create file" Action

**✅ Good news: Your HTTP trigger works! Now add SharePoint carefully:**

**Step-by-step setup:**

1. **Add action** → Search for "SharePoint" → Choose **"Create file"**

2. **Site Address:** 
   - Click the dropdown
   - Select: `https://fortive.sharepoint.com/sites/FTV-TheFort`
   - If it doesn't appear, you may need to click "Enter custom value" and paste it

3. **Folder Path:**
   - ⚠️ If folder browser doesn't show folders (permission issue):
   - Click "Enter custom value" 
   - Manually type the FULL path starting with `/Shared Documents`
   - Your folder path: `/Shared Documents/_2025/Projects/KATA/KATA Bugs Testing Automation`
   - ⚠️ Make sure spaces and special characters are typed exactly!
   - Do NOT use URL encoding (%20) - use actual spaces

4. **File Name:**
   - Click in the field → "Dynamic content" tab
   - Select **filename** from the HTTP trigger
   - Result should look like: `@{triggerBody()?['filename']}`

5. **File Content:** ⚠️ CRITICAL - Do this carefully:
   - Click in the field → Switch to **"Expression"** tab
   - Type: `base64ToBinary(triggerBody()['fileContent'])`
   - Click **OK**
   - Final result: `@{base64ToBinary(triggerBody()['fileContent'])}`
   - ⚠️ NO `?` before the brackets!

### 3. Response Action

**Add a "Response" action after the SharePoint action:**
- Status Code: `200`
- Headers: (leave empty or add `Content-Type`: `application/json`)
- Body:
```json
{
  "success": true,
  "fileUrl": "@{outputs('Create_file')?['body/{Link}']}"
}
```

**Note:** Replace `'Create_file'` with the actual name of your SharePoint action if different.

### 4. Common Issues to Check

❌ **Folder doesn't exist**
- Make sure the folder path exists in SharePoint
- Create the folder first if needed: `/Shared Documents/API Reports`

❌ **No permissions**
- The flow needs permission to write to that SharePoint location
- Check if the flow bot has access

❌ **Wrong expression syntax**
- File Content MUST use: `base64ToBinary(triggerBody()['fileContent'])` ← **NO question mark!**
- The `?` makes it optional and can return Null
- NOT: `triggerBody()?['fileContent']` ← This causes the Null error
- Enter it as an Expression, not Dynamic Content

❌ **Missing Response action**
- Without this, the flow might not return properly
- Always add a Response action as the last step

### 5. Test the Flow

**Option A: Test in Power Automate**
1. Click "Test" in the flow editor
2. Choose "Manually"
3. Click "Test"
4. Click "Run flow"
5. Enter test JSON:
```json
{
  "filename": "test.txt",
  "fileContent": "SGVsbG8gV29ybGQh",
  "timestamp": "2025-11-25"
}
```
6. Check if it succeeds

**Option B: Check Run History**
1. Go to the flow's main page
2. Click on "Run history"
3. Look at the failed runs with tracking IDs:
   - `b818807b-d053-4fe8-806d-639b74dc4b55`
   - `52cfb92b-260f-4fa5-83c1-b9cdc29ef9fe`
   - `6b9fd073-36cf-4bb3-80cb-b1592e001c70`
4. Click on them to see the exact error
5. Look for which step is failing

### 6. Alternative: Simpler Flow for Testing

If still having issues, try this minimal flow first:

**Step 1: HTTP Trigger**
- Use same JSON schema as above

**Step 2: Response** (skip SharePoint for now)
```json
{
  "received": "yes",
  "filename": "@{triggerBody()?['filename']}",
  "timestamp": "@{triggerBody()?['timestamp']}"
}
```

Test if this works first. If it does, then add the SharePoint action back.

---

## Once Fixed

After fixing the flow, run this command to test:
```bash
python test_flow_simple.py
```

You should see HTTP 200 instead of HTTP 500.

Then we can proceed with the full integration!
