"""
Simple Power Automate Flow Test
"""
import requests
import json

FLOW_URL = 'https://default0f634ac3b39f41a683ba8f107876c6.92.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/ba32c921bc9645aa889b6e147082b435/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=EazBMjq9CYJiZC_CU2s0n1WKCaqpZ7goHUN3LM7GzXk'

print('🧪 Testing Power Automate Flow\n')

# Test 1: Simple payload
print('Test 1: Minimal payload')
print('-' * 50)
payload1 = {
    "filename": "test.txt",
    "fileContent": "SGVsbG8gV29ybGQh",  # "Hello World!" in base64
    "timestamp": "2025-11-25_14-00-00"
}

try:
    response = requests.post(FLOW_URL, json=payload1, timeout=30)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text[:500]}\n')
except Exception as e:
    print(f'Error: {e}\n')

# Test 2: Check if flow accepts ANY request
print('Test 2: Empty payload')
print('-' * 50)
try:
    response = requests.post(FLOW_URL, json={}, timeout=30)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text[:500]}\n')
except Exception as e:
    print(f'Error: {e}\n')

print('='*60)
print('INSTRUCTIONS:')
print('='*60)
print('''
If both tests fail with 500 error, check your Power Automate flow:

1. Go to https://make.powerautomate.com
2. Find your flow: "Upload API Report to SharePoint"
3. Click "Edit"
4. Check the HTTP trigger - is the JSON schema correct?
5. Check the SharePoint action - verify:
   - Site Address is correct
   - Folder Path exists
   - File Name expression: @{triggerBody()?['filename']}
   - File Content expression: @{base64ToBinary(triggerBody()?['fileContent'])}
6. Check the Response action - is it configured?
7. Save and test again

Common issues:
- SharePoint folder path doesn't exist
- Flow bot doesn't have permission to the folder
- base64ToBinary expression is wrong
- Response action not configured correctly
''')
