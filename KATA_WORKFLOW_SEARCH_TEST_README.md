# KATA Workflow Search Functionality Test

## Overview

This test suite is designed to test the KATA workflow search API endpoint locally and store results in an Excel file for analysis.

**API Endpoint:** `https://kata-workflow-d7hncaeta9cra7a8.eastus-01.azurewebsites.net/api/kata_workflow`

## Files

1. **test_kata_workflow_search.py** - Python test script
2. **kata_workflow_search_results.xlsx** - Excel output with test results
3. **kata_workflow_test_queries.xlsx** - (Optional) Custom test queries template

## Quick Start

### 1. Install Dependencies
```bash
pip install requests openpyxl
```

### 2. Run Test
```bash
python3 test_kata_workflow_search.py
```

### 3. View Results
Open `kata_workflow_search_results.xlsx` in Excel or Google Sheets.

## Current Status

⚠️ **Authentication Issue**: The API endpoint returns `401 Unauthorized` with current credentials.

**Possible Solutions:**
1. **Different API Key**: The endpoint may require a different API key than the standard KATA endpoints
2. **Bearer Token**: May need OAuth or Bearer token authentication
3. **API Key Header**: Might expect `X-API-Key` header instead of form-urlencoded payload
4. **IP Whitelist**: Endpoint may be restricted to specific IPs
5. **Different Auth Method**: May use Azure AD or other authentication

## Excel Output Structure

The generated Excel file contains two sheets:

### Sheet 1: Summary
- Total tests run
- Success/failure counts
- Success rate percentage
- Test timestamp
- API endpoint URL

### Sheet 2: KATA Workflow Search Tests
| Column | Description |
|--------|-------------|
| # | Test number |
| Query | Search query tested |
| Status | success/error |
| Status Code | HTTP status code |
| Response | API response or error message |
| Sources | List of sources (if available) |
| Payload Variant | Which payload format was attempted |
| Timestamp | When the test was run |

## Customizing Tests

Edit the `TEST_QUERIES` list in `test_kata_workflow_search.py`:

```python
TEST_QUERIES = [
    "Your custom query 1",
    "Your custom query 2",
    # Add more queries...
]
```

## Test Results

**Latest Test Run:**
- Date: 2026-02-13
- Total Tests: 10
- Successful: 0 (all failed with 401 Unauthorized)
- Failed: 10
- Success Rate: 0%

**Error Details:**
All requests returned HTTP 401 Unauthorized, indicating authentication credentials need to be verified/updated for this specific endpoint.

## Next Steps

1. **Verify API Credentials**: Check if this endpoint requires different credentials
2. **Check API Documentation**: Request API docs or Swagger/OpenAPI spec for this endpoint
3. **Test with Postman/Insomnia**: Test manually to determine correct auth method
4. **Contact API Owner**: Confirm authentication requirements for `/api/kata_workflow`
5. **Check Headers**: May need additional headers like `Authorization: Bearer <token>`

## Authentication Attempts Made

The test script tries multiple payload formats:

1. **Standard Format** (from integrated_test_comparison.py)
   - email_id, question, session_id, conversation_id, agent_id, etc.

2. **Simplified Format**
   - email_id, question, session_id only

3. **Search-Specific Format**
   - email_id, query, session_id, conversation_id

All variants failed with 401, suggesting header-based authentication may be required.

## Support

For questions or issues:
1. Check the main testing framework: `integrated_test_comparison.py`
2. Review API configuration in the main codebase
3. Verify credentials with API team

---

**Created:** February 13, 2026  
**Purpose:** Local testing of KATA workflow search functionality  
**Author:** KATA Testing Framework Team
