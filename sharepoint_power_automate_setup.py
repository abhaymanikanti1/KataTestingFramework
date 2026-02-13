"""
SharePoint Upload via Power Automate - Configuration
"""

# Power Automate Flow Setup Instructions
POWER_AUTOMATE_SETUP = """
1. Go to https://make.powerautomate.com
2. Click "Create" → "Instant cloud flow"
3. Name it: "Upload API Report to SharePoint"
4. Choose trigger: "When a HTTP request is received"
5. Click "Create"

FLOW CONFIGURATION:

Step 1: HTTP Trigger
- In the trigger, click "Generate from sample"
- Paste this JSON:
{
  "filename": "Degraded_Responses_Report.xlsx",
  "fileContent": "base64-encoded-file-content-here",
  "timestamp": "2024-11-25_14-30-00"
}

Step 2: Add Action → SharePoint
- Search for "Create file" (SharePoint)
- Configure:
  * Site Address: https://fortive.sharepoint.com/sites/FTV-TheFort
  * Folder Path: Browse to your folder or use: /Shared Documents/API Reports
  * File Name: @{triggerBody()?['filename']}
  * File Content: @{base64ToBinary(triggerBody()?['fileContent'])}

Step 3: Add Action → Response
- Status Code: 200
- Body (JSON):
{
  "success": true,
  "fileUrl": "@{outputs('Create_file')?['body/{Link}']}"
}

Step 4: Save and Copy URL
- Click "Save" 
- Go back to the HTTP trigger
- Copy the "HTTP POST URL"
- Share that URL with me!
"""

# Python code will send file like this:
EXAMPLE_REQUEST = """
import requests
import base64

# Read the Excel file
with open('Degraded_Responses_Report.xlsx', 'rb') as f:
    file_content = base64.b64encode(f.read()).decode('utf-8')

# Send to Power Automate
payload = {
    "filename": "Degraded_Responses_Report.xlsx",
    "fileContent": file_content,
    "timestamp": "2024-11-25_14-30-00"
}

response = requests.post(
    "YOUR_POWER_AUTOMATE_URL",
    json=payload,
    headers={"Content-Type": "application/json"}
)

# Get SharePoint URL from response
sharepoint_url = response.json()['fileUrl']
print(f"Uploaded to: {sharepoint_url}")
"""

if __name__ == "__main__":
    print(POWER_AUTOMATE_SETUP)
    print("\n" + "="*60)
    print("EXAMPLE PYTHON CODE TO SEND FILE:")
    print("="*60)
    print(EXAMPLE_REQUEST)
