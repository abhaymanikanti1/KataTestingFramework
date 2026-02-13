"""
Test SharePoint Upload via Power Automate
"""
import requests
import base64
import os
from datetime import datetime

# Power Automate Workflow URL
SHAREPOINT_UPLOAD_URL = 'https://default0f634ac3b39f41a683ba8f107876c6.92.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/ba32c921bc9645aa889b6e147082b435/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=EazBMjq9CYJiZC_CU2s0n1WKCaqpZ7goHUN3LM7GzXk'

# Test file - use compare.xlsx as a test
TEST_FILE = 'compare.xlsx'

print('🧪 Testing SharePoint Upload via Power Automate\n')

if not os.path.exists(TEST_FILE):
    print(f'❌ Test file not found: {TEST_FILE}')
    exit(1)

print(f'📄 Test file: {TEST_FILE}')
print(f'📦 File size: {os.path.getsize(TEST_FILE):,} bytes\n')

try:
    # Read and encode file
    print('🔄 Reading and encoding file...')
    with open(TEST_FILE, 'rb') as f:
        file_content = base64.b64encode(f.read()).decode('utf-8')
    
    print(f'✅ Encoded {len(file_content):,} characters\n')
    
    # Prepare payload
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"TEST_{timestamp}_compare.xlsx"
    
    payload = {
        "filename": filename,
        "fileContent": file_content,  # Full file now!
        "timestamp": timestamp
    }
    
    print(f'📤 Uploading to SharePoint...')
    print(f'   Filename: {filename}')
    print(f'   Timestamp: {timestamp}')
    print(f'   Content length: {len(payload["fileContent"]):,} chars\n')
    
    # Send to Power Automate
    response = requests.post(
        SHAREPOINT_UPLOAD_URL,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    print(f'📡 Response Status: {response.status_code}')
    
    if response.status_code == 200:
        print('✅ Upload successful!\n')
        
        try:
            result = response.json()
            print('📋 Response Data:')
            print(f'   {result}\n')
            
            if 'fileUrl' in result:
                print(f'🔗 SharePoint URL:')
                print(f'   {result["fileUrl"]}\n')
                print('✅ File uploaded and URL received!')
            else:
                print('⚠️  Response received but no fileUrl in response')
                
        except Exception as e:
            print(f'⚠️  Response text: {response.text}')
            print(f'Note: Could not parse JSON response: {e}')
    else:
        print(f'❌ Upload failed!')
        print(f'Response: {response.text}')
        
except Exception as e:
    print(f'\n❌ Error: {e}')
    import traceback
    traceback.print_exc()

print('\n' + '='*60)
print('Test Complete!')
