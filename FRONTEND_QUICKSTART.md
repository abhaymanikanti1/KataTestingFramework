# KATA Testing API - Frontend Team Quickstart

## 🎯 What You Need to Know

We've built a REST API that serves the degraded API responses data in JSON format for your frontend to consume.

---

## 🔗 API URL

### ✅ Production URL (Azure App Service)
```
https://kata-api-v2.azurewebsites.net
```

**⚠️ Current Status:** Deployed but needs environment variable configuration.  
**See:** [FIX_AZURE_ENV_VAR.md](FIX_AZURE_ENV_VAR.md) for setup instructions.

Test it (after configuration):
```bash
curl https://kata-api-v2.azurewebsites.net/api/health
curl https://kata-api-v2.azurewebsites.net/api/degraded-responses
```

### ✅ Local Development URL (Working Now)
```
http://localhost:8000
```
**Status:** Fully functional and connected to Azure Blob Storage.

**For team access:** Use `http://YOUR_LOCAL_IP:8000` if on same network.

---

## 📡 API Endpoints

### 1. Get All Degraded Responses
```
GET http://localhost:8000/api/degraded-responses
```

**Response:** JSON with all sheets (PSP, VSM, TPI)
```json
{
  "total_sheets": 3,
  "last_updated": "2026-02-12T22:28:13.307954",
  "sheets": {
    "PSP Mentor Prompts": {
      "sheet_name": "PSP Mentor Prompts",
      "row_count": 44,
      "data": [...]
    },
    "VSM Mentor Prompts": {...},
    "TPI Mentor Prompts": {...}
  }
}
```

### 2. Get Specific Sheet
```
GET http://localhost:8000/api/degraded-responses/PSP
GET http://localhost:8000/api/degraded-responses/VSM
GET http://localhost:8000/api/degraded-responses/TPI
```

**Response:** JSON with specific sheet data
```json
{
  "sheet_name": "PSP Mentor Prompts",
  "row_count": 44,
  "data": [
    {
      "SL": "1",
      "Prompts": "How do I identify if a problem is caused or created?",
      "Response": "To differentiate between caused and created problems...",
      "Sources": "https://fortive.sharepoint.com/...",
      "Status": "Bad",
      "Tester Remarks": "P.Lee\\nThis is the same as number 7 above.",
      "Developer Remarks": null,
      "Date": null
    }
  ]
}
```

### 3. API Health Check
```
GET http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-12T22:28:13.307954",
  "cache": {
    "status": "active",
    "last_updated": "2026-02-12T22:28:13.307954",
    "age_seconds": 45,
    "ttl_seconds": 300
  },
  "blob_storage": {
    "connected": true,
    "blob_exists": true,
    "blob_metadata": {
      "name": "degraded_responses.xlsx",
      "size": 116079,
      "last_modified": "2026-02-12T16:31:30+00:00"
    }
  }
}
```

### 4. API Information
```
GET http://localhost:8000/
```

### 5. Interactive Documentation
```
GET http://localhost:8000/docs
GET http://localhost:8000/redoc
```

---

## 💻 Frontend Integration Examples

### JavaScript Fetch
```javascript
const API_URL = 'http://localhost:8000';

// Get all degraded responses
async function getAllData() {
  const response = await fetch(`${API_URL}/api/degraded-responses`);
  const data = await response.json();
  
  console.log(`Total sheets: ${data.total_sheets}`);
  console.log(`Last updated: ${data.last_updated}`);
  
  // Access PSP data
  const pspData = data.sheets['PSP Mentor Prompts'].data;
  console.log(`PSP has ${pspData.length} degraded responses`);
  
  return data;
}

// Get specific sheet
async function getPSPData() {
  const response = await fetch(`${API_URL}/api/degraded-responses/PSP`);
  const data = await response.json();
  
  return data.data; // Array of degraded responses
}

// Use in your app
getAllData().then(data => {
  // Render your table/UI
  renderTable(data.sheets['PSP Mentor Prompts'].data);
});
```

### React Example
```jsx
import { useState, useEffect } from 'react';

function DegradedResponsesTable() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetch('http://localhost:8000/api/degraded-responses/PSP')
      .then(res => res.json())
      .then(data => {
        setData(data.data);
        setLoading(false);
      });
  }, []);
  
  if (loading) return <div>Loading...</div>;
  
  return (
    <table>
      <thead>
        <tr>
          <th>SL</th>
          <th>Prompts</th>
          <th>Response</th>
          <th>Status</th>
          <th>Tester Remarks</th>
        </tr>
      </thead>
      <tbody>
        {data.map(row => (
          <tr key={row.SL}>
            <td>{row.SL}</td>
            <td>{row.Prompts}</td>
            <td>{row.Response}</td>
            <td>{row.Status}</td>
            <td>{row['Tester Remarks']}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### Python Example
```python
import requests

API_URL = 'http://localhost:8000'

# Get all data
response = requests.get(f'{API_URL}/api/degraded-responses')
data = response.json()

print(f"Total sheets: {data['total_sheets']}")
for sheet_name, sheet_data in data['sheets'].items():
    print(f"{sheet_name}: {sheet_data['row_count']} rows")

# Get PSP data only
psp_response = requests.get(f'{API_URL}/api/degraded-responses/PSP')
psp_data = psp_response.json()['data']

for item in psp_data:
    print(f"Prompt: {item['Prompts']}")
    print(f"Status: {item['Status']}")
    print()
```

---

## 🔄 Data Updates

The API automatically updates when new data is uploaded:

1. **Automated Testing** runs `integrated_test_comparison.py`
2. **Degraded responses** are identified and saved
3. **Excel file** is uploaded to Azure Blob Storage
4. **API cache** refreshes every 5 minutes automatically
5. **Your frontend** gets fresh data on next request

You can also force a refresh:
```
POST http://localhost:8000/api/refresh
```

---

## 🎨 Data Structure

### Row Object
```typescript
interface DegradedResponse {
  SL: string;                    // Serial number
  Prompts: string;               // Test prompt/question
  Response: string;              // AI response
  Sources: string | null;        // Source URLs
  Status: "Bad" | "Good" | "Neutral";  // Response quality
  "Tester Remarks": string | null;     // Tester feedback
  "Developer Remarks": string | null;  // Developer notes
  Date: string | null;           // Date if applicable
}
```

### Sheet Object
```typescript
interface Sheet {
  sheet_name: string;
  row_count: number;
  data: DegradedResponse[];
}
```

### Full Response
```typescript
interface AllSheetsResponse {
  total_sheets: number;
  last_updated: string;
  sheets: {
    [sheetName: string]: Sheet;
  };
}
```

---

## 🚀 Getting Started

### Step 1: Test the API
```bash
curl http://localhost:8000/api/health
```

### Step 2: Fetch Sample Data
```bash
curl http://localhost:8000/api/degraded-responses/PSP | python3 -m json.tool | head -50
```

### Step 3: Integrate into Your Frontend
Use the examples above based on your framework.

### Step 4: Display in Table Format
Map the JSON fields to your table columns.

---

## 📊 Available Sheets

| Sheet Name | Endpoint Suffix | Description |
|-----------|----------------|-------------|
| PSP Mentor Prompts | `/PSP` | Problem Solving Process mentor responses |
| VSM Mentor Prompts | `/VSM` | Value Stream Mapping mentor responses |
| TPI Mentor Prompts | `/TPI` | Transactional Process Improvement responses |

---

## ⚡ Performance

- **Cache:** 5-minute cache (responses are fast)
- **Data Size:** ~116 KB (very light)
- **Response Time:** < 100ms typically
- **CORS:** Enabled (works from any domain)

---

## 🛠️ Troubleshooting

### API not responding?
```bash
# Check if server is running
curl http://localhost:8000/api/health

# If not, start it
./start_api_for_frontend.sh
```

### CORS issues?
The API has CORS enabled for all origins. If you still face issues, let us know.

### Need different data format?
Contact us - we can modify the API response structure.

### Want additional fields?
We can expose more data from the Excel file.

---

## 📞 Contact

For questions or issues:
- Check interactive docs: `http://localhost:8000/docs`
- Review API health: `http://localhost:8000/api/health`
- Contact: KATA Testing Team

---

## ✅ Quick Checklist for Frontend

- [ ] Test API health endpoint
- [ ] Fetch sample data from one endpoint
- [ ] Understand JSON structure
- [ ] Implement table rendering
- [ ] Handle loading states
- [ ] Add error handling
- [ ] Test with all three sheets (PSP, VSM, TPI)
- [ ] Confirm data refresh works

---

**API Version:** 1.0.0  
**Last Updated:** February 12, 2026  
**Status:** ✅ Ready for Frontend Integration
