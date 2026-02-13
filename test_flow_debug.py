"""
Test Power Automate Flow - Step by Step Debugging
"""
import requests
import json

FLOW_URL = 'https://default0f634ac3b39f41a683ba8f107876c6.92.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/ba32c921bc9645aa889b6e147082b435/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=EazBMjq9CYJiZC_CU2s0n1WKCaqpZ7goHUN3LM7GzXk'

print('🔍 Power Automate Flow Debugging\n')
print('='*60)

# Test 1: Just trigger - no body at all
print('\nTest 1: No body (trigger only)')
print('-'*60)
try:
    response = requests.post(FLOW_URL, timeout=30)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text[:300]}')
except Exception as e:
    print(f'Error: {e}')

# Test 2: Empty JSON body
print('\n\nTest 2: Empty JSON body')
print('-'*60)
try:
    response = requests.post(
        FLOW_URL, 
        json={},
        headers={'Content-Type': 'application/json'},
        timeout=30
    )
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text[:300]}')
except Exception as e:
    print(f'Error: {e}')

# Test 3: Minimal valid JSON (no base64)
print('\n\nTest 3: Minimal JSON (just strings)')
print('-'*60)
payload = {
    "filename": "test.txt",
    "fileContent": "Hello World",
    "timestamp": "2025-11-25"
}
try:
    response = requests.post(
        FLOW_URL,
        json=payload,
        headers={'Content-Type': 'application/json'},
        timeout=30
    )
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text[:300]}')
except Exception as e:
    print(f'Error: {e}')

print('\n' + '='*60)
print('DIAGNOSIS:')
print('='*60)
print('''
If ALL tests show 500 error:
→ The flow itself has a configuration error
→ Check Power Automate Run History with these tracking IDs
→ Look at which ACTION is failing (not just the trigger)

Go to: https://make.powerautomate.com
→ Your flow → Run history
→ Click on the failed runs
→ Look for RED X icons to see which step failed

Common causes:
1. SharePoint site/folder doesn't exist or wrong path
2. Flow doesn't have permission to SharePoint site
3. SharePoint action is trying to evaluate expression before receiving data
4. Response action has syntax error

RECOMMENDATION:
Temporarily REMOVE the SharePoint action completely.
Keep only: HTTP Trigger → Response
Test if that works.
If yes, add SharePoint action back step by step.
''')
