"""
Test if a simple text file works correctly through the upload
"""
import requests
import base64
from datetime import datetime

FLOW_URL = 'https://default0f634ac3b39f41a683ba8f107876c6.92.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/ba32c921bc9645aa889b6e147082b435/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=EazBMjq9CYJiZC_CU2s0n1WKCaqpZ7goHUN3LM7GzXk'

print('🧪 Testing Simple Text File Upload\n')

# Create a simple text file
test_content = "This is a test file.\nLine 2\nLine 3\nIf you can read this, the upload works!"

# Encode to base64
encoded = base64.b64encode(test_content.encode('utf-8')).decode('utf-8')

print(f'Original text: {test_content}')
print(f'Base64: {encoded}\n')

# Upload
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
payload = {
    "filename": f"TEST_{timestamp}_simple.txt",
    "fileContent": encoded,
    "timestamp": timestamp
}

print('📤 Uploading to SharePoint...')
response = requests.post(FLOW_URL, json=payload, timeout=30)

print(f'Status: {response.status_code}')
if response.status_code == 200:
    result = response.json()
    file_path = result.get('fileUrl', '')
    print(f'✅ Upload successful!')
    print(f'📁 File: {file_path}')
    print(f'\n🔗 Go to SharePoint and open this file:')
    print(f'   https://fortive.sharepoint.com/:f:/r/sites/FTV-TheFort/Shared%20Documents/_2025/Projects/KATA/KATA%20Bugs%20Testing%20Automation')
    print(f'\n✅ If you can read the text above, base64 encoding/decoding works!')
    print(f'❌ If the file is corrupted, the Flow\'s File Content expression is wrong.')
else:
    print(f'❌ Upload failed: {response.text}')
