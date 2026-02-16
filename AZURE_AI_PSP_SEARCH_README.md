# Azure AI PSP Search Test Guide

## Overview

This test script queries the Azure AI KATA API using PSP Mentor prompts from your benchmark file and saves results to Excel.

## Quick Start

```bash
# 1. Ensure Azure CLI is installed and logged in
az login

# 2. Run the test
python3 test_azure_ai_psp_search.py
```

## What It Does

1. **Fetches Bearer Token** automatically using Azure CLI:
   ```bash
   az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv
   ```

2. **Loads PSP Questions** from `compare.xlsx` (sheet: "PSP Mentor Prompts")

3. **For Each Question**:
   - Creates a conversation with agent "shikha-exp-v3"
   - Sends the question to the agent
   - Collects the response and sources
   
4. **Generates Excel Report**: `azure_ai_psp_search_results.xlsx`

## API Endpoints Used

### 1. Create Conversation
```
POST https://aif-kata2.services.ai.azure.com/api/projects/kataproject/openai/conversations
```

**Request:**
```json
{
  "conversation": "",
  "input": "Hi shikha-exp-v3",
  "stream": false,
  "agent": {
    "name": "shikha-exp-v3",
    "type": "agent_reference"
  }
}
```

### 2. Query Agent
```
POST https://aif-kata2.services.ai.azure.com/api/projects/kataproject/openai/responses
```

**Request:**
```json
{
  "conversation": "<conversation_id_from_step_1>",
  "input": "<your_question>",
  "stream": false,
  "agent": {
    "name": "shikha-exp-v3",
    "type": "agent_reference"
  }
}
```

## Bearer Token

**Expiration:** 1 hour

**Regenerate:** 
```bash
az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv
```

The script automatically fetches a fresh token when run.

## Output File Structure

**File:** `azure_ai_psp_search_results.xlsx`

### Sheet 1: Summary
- Total tests
- Success/failure counts
- Success rate
- Test timestamp
- API endpoint info

### Sheet 2: PSP Search Test Results

| Column | Description |
|--------|-------------|
| # | Test number |
| Benchmark Row | Row number in compare.xlsx |
| Question | PSP query tested |
| Status | success or error |
| Status Code | HTTP status code |
| Response | Agent's answer |
| Sources | Citations/sources provided |
| Conversation ID | Azure conversation ID |
| Timestamp | When test ran |

## Configuration

Edit these variables in `test_azure_ai_psp_search.py`:

```python
# Azure AI endpoints
AZURE_AI_BASE_URL = "https://aif-kata2.services.ai.azure.com/api/projects/kataproject/openai"
API_VERSION = "2025-11-15-preview"
AGENT_NAME = "shikha-exp-v3"

# Local files
BENCHMARK_FILE = "compare.xlsx"
PSP_SHEET_NAME = "PSP Mentor Prompts"
OUTPUT_FILE = "azure_ai_psp_search_results.xlsx"
```

## Troubleshooting

### Error: "Azure CLI not found"
**Solution:** Install Azure CLI
- Mac: `brew install azure-cli`
- Windows: Download from https://aka.ms/installazurecliwindows
- Linux: https://docs.microsoft.com/cli/azure/install-azure-cli-linux

### Error: "Failed to obtain bearer token"
**Solution:** Login to Azure
```bash
az login
az account set --subscription "<your-subscription-id>"
```

### Error: "Sheet 'PSP Mentor Prompts' not found"
**Solution:** Verify benchmark file exists
```bash
ls -l compare.xlsx
```

Check sheet names match exactly (case-sensitive).

### Error: "Failed to create conversation"
**Possible causes:**
1. Bearer token expired (regenerate)
2. Network connectivity issues
3. API endpoint changed
4. Insufficient permissions

**Debug:**
```bash
# Test token manually
TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)
echo $TOKEN

# Test API manually
curl --request POST \
  --url 'https://aif-kata2.services.ai.azure.com/api/projects/kataproject/openai/conversations?api-version=2025-11-15-preview' \
  --header "Authorization: Bearer $TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{
    "conversation": "",
    "input": "test",
    "stream": false,
    "agent": {"name": "shikha-exp-v3", "type": "agent_reference"}
  }'
```

## Comparison with Original Test

### Old Workflow API Test
- Endpoint: `https://kata-workflow-d7hncaeta9cra7a8.eastus-01.azurewebsites.net/api/kata_workflow`
- Auth: Form-urlencoded credentials
- Status: 401 Unauthorized ❌

### New Azure AI Test  
- Endpoint: `https://aif-kata2.services.ai.azure.com/api/projects/kataproject/openai/`
- Auth: Bearer token (Azure AD)
- Status: Should work ✅

## Sample Output

```
================================================================================
Azure AI KATA Search Test - PSP Mentor Queries
================================================================================
API Endpoint: https://aif-kata2.services.ai.azure.com/api/projects/kataproject/openai
Agent: shikha-exp-v3
Benchmark File: compare.xlsx
Output File: azure_ai_psp_search_results.xlsx
================================================================================

🔑 Fetching Azure bearer token...
✅ Bearer token obtained successfully

📂 Loading queries from compare.xlsx...
✅ Found Prompt column at index 2
✅ Loaded 47 PSP Search queries

📊 Testing 47 PSP Search queries...

[1/47] Row 2: What is PSP?...
  → Creating conversation...
  ✅ Conversation created: conv_abc123
  → Querying agent...
  ✅ Success! Response: PSP (Personal Software Process) is a structured framework...

...

================================================================================
TEST SUMMARY
================================================================================
Total Tests: 47
✅ Successful: 45
❌ Failed: 2
Success Rate: 95.7%
================================================================================

📁 Results: azure_ai_psp_search_results.xlsx
```

## Next Steps

1. **Run the test** to generate results
2. **Open Excel file** to review responses
3. **Compare with benchmarks** in your existing framework
4. **Integrate** into `integrated_test_comparison.py` if needed

## Integration with Main Framework

To use this Azure AI endpoint in your main testing framework:

1. Update `integrated_test_comparison.py`:
   - Replace old API endpoint
   - Add Bearer token authentication
   - Implement two-step conversation flow

2. Update GitHub Actions workflows:
   - Add Azure login step 
   - Fetch bearer token before tests
   - Handle token expiration

---

**Created:** February 13, 2026  
**Purpose:** Test Azure AI KATA API with PSP Search queries  
**Author:** KATA Testing Framework Team
