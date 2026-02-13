"""
Test the Teams alert function with simulated degraded responses
"""
import sys
sys.path.insert(0, '/Users/abhay.manikanti/Documents/untitled folder')

from integrated_test_comparison import send_teams_alert

# Simulate degraded responses
fake_degraded_responses = [
    {
        'sheet_name': 'PSP Mentor',
        'serial': 5,
        'prompt': 'What is the DIVE process in PSP?',
        'reason': 'Response is 60% shorter than benchmark',
        'severity': 'HIGH'
    },
    {
        'sheet_name': 'VSM Mentor',
        'serial': 12,
        'prompt': 'Explain value stream mapping',
        'reason': 'New response contains generic content',
        'severity': 'MEDIUM'
    },
    {
        'sheet_name': 'TPI Mentor',
        'serial': 8,
        'prompt': 'What are TPI best practices?',
        'reason': 'Missing key keywords from original response',
        'severity': 'MEDIUM'
    }
]

print('🧪 Testing Teams Alert with Simulated Degraded Responses\n')
print(f'Simulating {len(fake_degraded_responses)} degraded responses...\n')

send_teams_alert(fake_degraded_responses)

print('\n✅ Test complete! Check your Teams channel for the alert.')
