"""
Test what the SharePoint action actually returns
"""
import requests
import base64

FLOW_URL = 'https://default0f634ac3b39f41a683ba8f107876c6.92.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/ba32c921bc9645aa889b6e147082b435/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=EazBMjq9CYJiZC_CU2s0n1WKCaqpZ7goHUN3LM7GzXk'

print('🔍 Testing SharePoint Response\n')

# Small test file
content = base64.b64encode(b"Hello World Test File").decode('utf-8')

payload = {
    "filename": "diagnostic_test.txt",
    "fileContent": content,
    "timestamp": "2025-11-25"
}

response = requests.post(FLOW_URL, json=payload, timeout=30)

print(f'Status: {response.status_code}')
print(f'\nFull Response Text:\n{response.text}')
print(f'\nFull Response JSON:\n{response.json()}')

print('\n' + '='*60)
print('INSTRUCTIONS:')
print('='*60)
print('''
Look at the response above. If fileUrl is empty, try these fixes:

In Power Automate Response action, try these Body options:

Option 1:
{
  "success": true,
  "fileUrl": "@{body('Create_file')?['Path']}"
}

Option 2:
{
  "success": true,
  "fileUrl": "@{outputs('Create_file')?['body']?['Path']}"
}

Option 3:
{
  "success": true,  
  "fileUrl": "@{body('Create_file')?['ServerRelativeUrl']}"
}

Option 4 (return everything to see what's available):
{
  "success": true,
  "allOutputs": "@{outputs('Create_file')}"
}
''')
