"""
Test Teams webhook with Adaptive Card format
"""
import requests
from datetime import datetime

WEBHOOK_URL = 'https://default0f634ac3b39f41a683ba8f107876c6.92.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/338930b654414d3fad97006b24eba22a/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=F2Sc96VixuuckIZy1e3Djtcx4JnOGmHDoQfleymy5-U'

print('🧪 Testing Adaptive Card Format for Teams\n')

# Build test message
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
message_text = f"""This is a test alert from the API Quality Monitor!

**Test Details:**
• Time: {timestamp}
• Status: Testing webhook integration
• Target: Kata Testers group chat

If you see this message, the webhook is working correctly! ✅"""

# Adaptive Card format matching Power Automate setup
payload = {
    'content': {
        'type': 'AdaptiveCard',
        'body': [
            {
                'type': 'TextBlock',
                'size': 'Large',
                'weight': 'Bolder',
                'text': '🧪 Test Alert from API Quality Monitor',
                'wrap': True,
                'color': 'Attention'
            },
            {
                'type': 'TextBlock',
                'text': message_text,
                'wrap': True
            }
        ],
        '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
        'version': '1.4'
    }
}

try:
    print('📤 Sending test card to Teams...')
    response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    
    print(f'✅ Status Code: {response.status_code}')
    
    if response.status_code in [200, 202]:
        print('\n✅ SUCCESS!')
        print('📱 Check your "Kata Testers" group chat in Teams for the test card!')
    else:
        print(f'\n⚠️  Unexpected status: {response.status_code}')
        print(f'Response: {response.text[:200]}')
        
except Exception as e:
    print(f'\n❌ ERROR: {type(e).__name__}: {e}')
