"""
Quick API test - Test single question with corrected parameters
"""
import requests
import urllib3
import urllib.parse
import uuid
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
API_URL = 'https://container-app-ui-stage.purplesky-e0183d2f.eastus.azurecontainerapps.io/api/pspmentor'
EMAIL_ID = 'abhay.manikanti@fortive.com'
SESSION_ID = '36f80c7f-e3ab-4c2b-b384-031cc0b6f8f3'

HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'insomnia/11.4.0'
}

def test_api():
    """Test API with a single question"""
    test_question = 'What is PSP?'
    
    payload_dict = {
        "email_id": EMAIL_ID,
        "question": test_question,
        "session_id": SESSION_ID,
        "conversation_id": str(uuid.uuid4()),
        "agent_id": "psp",
        "thread_id": "",
        "selected_column": "",
        "container": "useruploaded"
    }
    
    payload_encoded = urllib.parse.urlencode(payload_dict)
    
    print("="*70)
    print("🧪 Quick API Test")
    print("="*70)
    print(f"API: {API_URL}")
    print(f"Question: {test_question}")
    print(f"Session: {SESSION_ID}")
    print("="*70)
    print()
    
    try:
        print("📤 Sending request...")
        response = requests.post(
            API_URL, 
            data=payload_encoded, 
            headers=HEADERS, 
            verify=False, 
            timeout=60,
            stream=True
        )
        
        print(f"✅ Response received: {response.status_code}")
        
        if response.status_code == 200:
            print("📥 Parsing response...")
            
            # Collect response
            content_parts = []
            sources = []
            line_count = 0
            
            for line in response.iter_lines(decode_unicode=True):
                if line and line.strip():
                    line_count += 1
                    
                    if line.startswith('data: '):
                        json_part = line[6:].strip()
                        if json_part and json_part != '[DONE]':
                            try:
                                data_obj = json.loads(json_part)
                                
                                # NEW FORMAT: assistant_output directly in the object
                                if isinstance(data_obj, dict):
                                    if 'assistant_output' in data_obj and data_obj['assistant_output']:
                                        output = str(data_obj['assistant_output'])
                                        # Filter out initialization messages with emojis
                                        if not any(emoji in output for emoji in ['🔄', '🔧', '📋', '🔍', '📂', '🤔', '📚', '✨']):
                                            content_parts.append(output)
                                    
                                    # OLD FORMAT: Check nested 'data' key
                                    elif 'data' in data_obj and isinstance(data_obj['data'], dict):
                                        chunk_data = data_obj['data']
                                        if 'assistant_output' in chunk_data and chunk_data['assistant_output']:
                                            content_parts.append(str(chunk_data['assistant_output']))
                                        
                                        # Extract sources
                                        if 'sources' in chunk_data and isinstance(chunk_data['sources'], list):
                                            for source in chunk_data['sources']:
                                                if isinstance(source, dict):
                                                    for url_field in ['page_url', 'url', 'link']:
                                                        if url_field in source and source[url_field]:
                                                            sources.append(source[url_field])
                                                            break
                                    
                                    # Extract sources from top-level
                                    if 'sources' in data_obj and isinstance(data_obj['sources'], list):
                                        for source in data_obj['sources']:
                                            if isinstance(source, dict):
                                                for url_field in ['page_url', 'url', 'link']:
                                                    if url_field in source and source[url_field]:
                                                        sources.append(source[url_field])
                                                        break
                            except json.JSONDecodeError:
                                continue
            
            full_content = ''.join(content_parts)
            unique_sources = list(dict.fromkeys(sources))[:5]
            
            print()
            print("="*70)
            print("✅ SUCCESS!")
            print("="*70)
            print(f"Lines processed: {line_count}")
            print(f"Content length: {len(full_content)} chars")
            print(f"Sources found: {len(unique_sources)}")
            print()
            print("Response preview:")
            print("-"*70)
            print(full_content[:300] if full_content else "(No content)")
            print()
            if unique_sources:
                print("Sources:")
                for i, src in enumerate(unique_sources[:3], 1):
                    print(f"  {i}. {src}")
            print("="*70)
            
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text[:300])
            
    except requests.Timeout:
        print("❌ TIMEOUT: API did not respond within 60 seconds")
        print("\n⚠️  Possible issues:")
        print("   - API service may be down")
        print("   - Session ID may be expired")
        print("   - Network connectivity issues")
        print("   - Authentication required")
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_api()
