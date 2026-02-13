"""
Debug: Check file sizes and compare
"""
import os
import base64

# Check the local test file
local_file = 'TEST_Degraded_Responses_Report.xlsx'

if os.path.exists(local_file):
    file_size = os.path.getsize(local_file)
    print(f'Local file: {local_file}')
    print(f'File size: {file_size:,} bytes')
    
    # Read and encode
    with open(local_file, 'rb') as f:
        content = f.read()
        encoded = base64.b64encode(content).decode('utf-8')
    
    print(f'Encoded size: {len(encoded):,} characters')
    print(f'First 100 chars: {encoded[:100]}')
    print(f'Last 100 chars: {encoded[-100:]}')
    
    # Decode to verify
    decoded = base64.b64decode(encoded)
    print(f'\nDecoded size: {len(decoded):,} bytes')
    print(f'Matches original: {decoded == content}')
    
    if decoded == content:
        print('✅ Base64 encoding/decoding works correctly locally')
    else:
        print('❌ Base64 encoding/decoding is broken!')
else:
    print(f'❌ File not found: {local_file}')

print('\n' + '='*60)
print('NEXT STEP:')
print('='*60)
print('Go to SharePoint and check the file size of:')
print('2025-11-25_18-43-29_TEST_Degraded_Responses_Report.xlsx')
print('\nCompare it with the local file size above.')
print('If SharePoint file is much smaller, the upload is truncating data.')
