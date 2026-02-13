# 🎯 FOR FRONTEND TEAM - API URL & INTEGRATION

## ✅ API IS READY!

Your REST API for degraded responses data is fully functional and ready to use.

---

## 🔗 API URL TO GIVE FRONTEND TEAM

### **Current Working URL**
```
http://localhost:8000
```

### **Main Endpoint for All Data**
```
GET http://localhost:8000/api/degraded-responses
```

### **Individual Sheet Endpoints**
```
GET http://localhost:8000/api/degraded-responses/PSP
GET http://localhost:8000/api/degraded-responses/VSM  
GET http://localhost:8000/api/degraded-responses/TPI
```

### **Interactive Documentation**
```
http://localhost:8000/docs
```
_(Share this URL - frontend team can test API directly in browser!)_

---

## 🚀 How to Start the API Server

```bash
cd /Users/abhay.manikanti/Downloads/KataTestingFramework-main
./start_api_for_frontend.sh
```

The server will run on `http://localhost:8000` and automatically connect to Azure Blob Storage.

---

## 📋 What Frontend Team Gets

### JSON Response Example (PSP Sheet)
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
    },
    // ... more rows
  ]
}
```

---

## 🎨 Quick Frontend Integration

### JavaScript
```javascript
fetch('http://localhost:8000/api/degraded-responses/PSP')
  .then(res => res.json())
  .then(data => {
    console.log(`Loaded ${data.row_count} rows`);
    // Render your table with data.data
  });
```

### Full documentation
See `FRONTEND_QUICKSTART.md` for complete integration examples.

---

## 🔄 How Data Updates Work

1. **You run** `python3 integrated_test_comparison.py`
2. **Script tests** all API responses
3. **Identifies** degraded responses (Bad status)
4. **Uploads** to Azure Blob Storage
5. **API automatically** serves the new data (refreshes every 5 min)
6. **Frontend** gets updated data on next request

---

## ✅ Current Status

- ✅ API Server: **Working**
- ✅ Azure Blob Storage: **Connected**
- ✅ Data File: **116 KB, 3 sheets**
- ✅ Endpoints: **All functional**
- ✅ CORS: **Enabled**
- ✅ Documentation: **Available at /docs**

---

## 🌐 Options for External Access

### Option 1: Local (Current)
- URL: `http://localhost:8000`
- Works immediately
- Only accessible on your machine

### Option 2: ngrok (Temporary External)
```bash
# Install ngrok
brew install ngrok

# Expose local API
ngrok http 8000

# Get public URL like: https://abcd-12-34-56-78.ngrok-free.app
# Share with frontend team
```

### Option 3: Azure (Production - In Progress)
- URL: `https://kata-api-v2.azurewebsites.net`
- Status: Deployment in progress
- Will be available soon

---

## 📞 Tell Frontend Team

**"The API is ready! Here's what you need:"**

1. **Base URL:** `http://localhost:8000`

2. **Main Endpoint:** `GET /api/degraded-responses/PSP` (or VSM, TPI)

3. **Test it:** Open `http://localhost:8000/docs` in browser

4. **JSON Structure:** See `FRONTEND_QUICKSTART.md`

5. **Examples:** JavaScript, React, Python examples provided

6. **Support:** API auto-refreshes data every 5 minutes

---

## 🎯 Next Steps

### For You
1. ✅ API is running locally
2. ✅ Documentation created
3. ⏳ Azure deployment in progress (optional - local works fine)

### For Frontend Team
1. Access `http://localhost:8000/docs` to see/test API
2. Read `FRONTEND_QUICKSTART.md` for integration examples
3. Start fetching data and building UI
4. Contact if they need any changes to JSON structure

---

## 📁 Files Created for Frontend Team

1. **FRONTEND_QUICKSTART.md** - Complete integration guide
2. **API_DEPLOYMENT_GUIDE.md** - Technical deployment details
3. **start_api_for_frontend.sh** - Easy server startup script

---

**🎉 You're all set! The frontend team can start integrating immediately.**

Share these URLs with them:
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health
- **PSP Data:** http://localhost:8000/api/degraded-responses/PSP
