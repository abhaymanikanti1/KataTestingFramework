"""
Test the new Teams webhook - including file attachment attempt
Note: Office 365 Incoming Webhooks don't support direct file uploads
We'll include a file reference/link in the message instead
"""
import requests
import os
from datetime import datetime

WEBHOOK_URL = 'https://fortive.webhook.office.com/webhookb2/199c08e6-d1b2-4042-86ae-db6675d663a2@0f634ac3-b39f-41a6-83ba-8f107876c692/IncomingWebhook/97923a6885004ab5acb19d16cea887e4/91b293f9-febd-40ad-ba66-36b2f7f5c200/V2EHCUUYb6H_WLAVlnhmUcZL59FLN3XAJSByqFWmonaPI1'

print('🧪 Testing Office 365 Incoming Webhook\n')

# Office 365 webhooks use MessageCard format (not Adaptive Card)
message_card = {
    "@type": "MessageCard",
    "@context": "https://schema.org/extensions",
    "summary": "Test Alert from API Quality Monitor",
    "themeColor": "0078D7",
    "title": "🧪 Test Alert: Webhook Connection Verified!",
    "sections": [
        {
            "activityTitle": "API Quality Monitor Test",
            "activitySubtitle": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "activityImage": "https://adaptivecards.io/content/cats/1.png",
            "facts": [
                {
                    "name": "Status:",
                    "value": "✅ Webhook working!"
                },
                {
                    "name": "Test Type:",
                    "value": "MessageCard Format"
                },
                {
                    "name": "File Reference:",
                    "value": "Degraded_Responses_Report.xlsx"
                }
            ],
            "text": "This is a test message to verify the Office 365 Incoming Webhook is working correctly. \\n\\n**Note:** Incoming webhooks cannot directly attach files, but can include links or references."
        }
    ],
    "potentialAction": [
        {
            "@type": "OpenUri",
            "name": "View Documentation",
            "targets": [
                {
                    "os": "default",
                    "uri": "https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using"
                }
            ]
        }
    ]
}

try:
    print('📤 Sending MessageCard to Teams...')
    response = requests.post(WEBHOOK_URL, json=message_card, timeout=10)
    
    print(f'✅ Status Code: {response.status_code}')
    
    if response.status_code == 200:
        print('\n✅ SUCCESS!')
        print('📱 Check your Teams channel for the message card!')
        print('\n⚠️  Note: Office 365 Incoming Webhooks do NOT support file attachments.')
        print('   Files must be uploaded separately or shared via link.')
    else:
        print(f'\n⚠️  Unexpected status: {response.status_code}')
        print(f'Response: {response.text[:200]}')
        
except Exception as e:
    print(f'\n❌ ERROR: {type(e).__name__}: {e}')

print('\n' + '='*70)
print('WEBHOOK CAPABILITIES:')
print('='*70)
print('✅ Can send: Rich MessageCard format with sections, facts, buttons')
print('✅ Can send: Links to files (users click to open)')
print('❌ Cannot send: Direct file attachments')
print('\nRecommendation: Include SharePoint/OneDrive link to Excel file')
print('='*70)
