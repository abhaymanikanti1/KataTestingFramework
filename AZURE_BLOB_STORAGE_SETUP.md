# Azure Blob Storage Setup for Excel File Upload

## Why Blob Storage (Not Cosmos DB)?

**Azure Blob Storage** is the correct choice for storing Excel files:
- ✅ Designed for file storage (Excel, PDF, images, etc.)
- ✅ Simple file upload/download/overwrite operations
- ✅ Very cost-effective (~$0.02/GB/month)
- ✅ Direct download URLs for Teams notifications
- ✅ Versioning support (optional)

**Cosmos DB is NOT suitable** - it's for JSON document databases, not files.

---

## Step 1: Create Storage Account

### Via Azure Portal:

1. **Go to:** https://portal.azure.com
2. **Search:** "Storage accounts" → **Create**
3. **Fill in:**
   - **Subscription:** Your Fortive subscription
   - **Resource Group:** Create new or use existing (e.g., `kata-testing-rg`)
   - **Storage account name:** `katatestingstorage` (must be globally unique, lowercase, no spaces)
   - **Region:** East US (or closest to your app)
   - **Performance:** Standard
   - **Redundancy:** LRS (Locally Redundant Storage) - cheapest option
4. **Click:** Review + Create → Create
5. **Wait** for deployment to complete (~1 minute)

---

## Step 2: Create Blob Container

1. **Go to** your new storage account
2. **Left menu:** Containers (under Data storage)
3. **Click:** + Container
4. **Name:** `kata-reports` (or any name you prefer)
5. **Public access level:** 
   - **Private** (recommended - requires authentication)
   - OR **Blob** (anonymous read access for direct links)
6. **Click:** Create

---

## Step 3: Get Connection String

1. **In your storage account** → Left menu → **Access keys**
2. **Click:** Show keys
3. **Copy** the **Connection string** under **key1**
   - It looks like: `DefaultEndpointsProtocol=https;AccountName=katatestingstorage;AccountKey=...;EndpointSuffix=core.windows.net`
4. **Save this securely** - you'll need it for Python code

---

## Step 4: Install Python SDK

Add to `requirements.txt`:

```txt
azure-storage-blob>=12.19.0
```

Install:
```bash
pip install azure-storage-blob
```

---

## Step 5: Python Code to Upload Excel File

Create `upload_to_blob.py`:

```python
from azure.storage.blob import BlobServiceClient
import os
from datetime import datetime

# Configuration
CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', 'your-connection-string-here')
CONTAINER_NAME = 'kata-reports'
BLOB_NAME = 'Degraded_Responses_Report.xlsx'  # Fixed filename - will overwrite

def upload_excel_to_blob(local_file_path, blob_name=BLOB_NAME):
    """
    Upload Excel file to Azure Blob Storage
    - Will overwrite existing file with same name
    - Returns public URL if container is public, or SAS URL
    """
    try:
        # Create BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        
        # Get container client
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        # Get blob client
        blob_client = container_client.get_blob_client(blob_name)
        
        # Upload file (overwrite if exists)
        print(f"Uploading {local_file_path} to Azure Blob Storage...")
        with open(local_file_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        
        # Get blob URL
        blob_url = blob_client.url
        print(f"✅ Upload successful!")
        print(f"📁 Blob URL: {blob_url}")
        
        return blob_url
        
    except Exception as e:
        print(f"❌ Error uploading to Blob Storage: {e}")
        return None

# Example usage
if __name__ == "__main__":
    local_file = "Degraded_Responses_Report.xlsx"
    
    if os.path.exists(local_file):
        url = upload_excel_to_blob(local_file)
        if url:
            print(f"\n🔗 File available at: {url}")
    else:
        print(f"❌ File not found: {local_file}")
```

---

## Step 6: Integrate with Your Code

Update `integrated_test_comparison.py`:

**Option A: Replace SharePoint upload with Blob Storage**

```python
# At the top of the file
from azure.storage.blob import BlobServiceClient
import os

# Configuration
AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
BLOB_CONTAINER_NAME = 'kata-reports'
BLOB_NAME = 'Degraded_Responses_Report.xlsx'

def upload_to_blob_storage(file_path):
    """Upload Excel file to Azure Blob Storage"""
    
    if not AZURE_STORAGE_CONNECTION_STRING:
        print("\n  ⚠️  Azure Storage connection string not configured")
        return None
    
    if not os.path.exists(file_path):
        print(f"\n  ⚠️  File not found: {file_path}")
        return None
    
    try:
        print(f"\n  📤 Uploading {os.path.basename(file_path)} to Azure Blob Storage...")
        
        # Create clients
        blob_service_client = BlobServiceClient.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING
        )
        container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
        blob_client = container_client.get_blob_client(BLOB_NAME)
        
        # Upload (overwrite existing)
        with open(file_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        
        blob_url = blob_client.url
        
        print(f"  ✅ Uploaded successfully!")
        print(f"  🔗 Blob URL: {blob_url}")
        
        return blob_url
        
    except Exception as e:
        print(f"\n  ❌ Error uploading to Blob Storage: {e}")
        return None
```

Then in the `main()` function, replace:
```python
sharepoint_url = upload_to_sharepoint(DEGRADED_OUTPUT_FILE)
```

With:
```python
blob_url = upload_to_blob_storage(DEGRADED_OUTPUT_FILE)
```

**Option B: Keep both (SharePoint + Blob Storage)**

Keep SharePoint for team access, use Blob Storage as backup/archive.

---

## Step 7: Set Environment Variable

### Locally:
```bash
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=katatestingstorage;AccountKey=...;EndpointSuffix=core.windows.net"
```

### GitHub Actions:
1. Go to your repo: Settings → Secrets and variables → Actions
2. Click **New repository secret**
3. Name: `AZURE_STORAGE_CONNECTION_STRING`
4. Value: Your connection string
5. Click **Add secret**

Update `.github/workflows/daily-kata-test.yml`:
```yaml
env:
  TZ: 'Asia/Kolkata'
  TEAMS_WEBHOOK_URL: ${{ secrets.TEAMS_WEBHOOK_URL }}
  SHAREPOINT_UPLOAD_URL: ${{ secrets.SHAREPOINT_UPLOAD_URL }}
  AZURE_STORAGE_CONNECTION_STRING: ${{ secrets.AZURE_STORAGE_CONNECTION_STRING }}
```

---

## Advanced: Generate SAS URL for Private Containers

If your container is private, generate a temporary access URL:

```python
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

def upload_with_sas_url(local_file_path, blob_name=BLOB_NAME):
    """Upload and generate SAS URL with 7-day expiry"""
    
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(CONTAINER_NAME, blob_name)
    
    # Upload
    with open(local_file_path, 'rb') as data:
        blob_client.upload_blob(data, overwrite=True)
    
    # Generate SAS token (7 days expiry)
    sas_token = generate_blob_sas(
        account_name=blob_client.account_name,
        container_name=CONTAINER_NAME,
        blob_name=blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(days=7)
    )
    
    sas_url = f"{blob_client.url}?{sas_token}"
    return sas_url
```

---

## Cost Estimate

**Storage:** ~$0.02/GB/month
- 1 MB Excel file = $0.00002/month
- 1000 files (1 GB) = $0.02/month

**Transactions:**
- Write operations: $0.05 per 10,000
- Read operations: $0.004 per 10,000

**Total monthly cost:** < $1 for typical usage

---

## File Versioning (Optional)

Enable versioning to keep history:

1. Storage account → Data management → **Data protection**
2. Enable **Blob versioning**
3. Set retention period (e.g., 30 days)

Every upload creates a new version instead of overwriting.

---

## What to Provide Me

To integrate this, provide:

1. ✅ **Connection String** from Access Keys section
2. ✅ **Container Name** (e.g., `kata-reports`)
3. ✅ **Blob Name** for the file (e.g., `Degraded_Responses_Report.xlsx`)
4. Do you want to:
   - **Replace** SharePoint upload with Blob Storage?
   - **Keep both** SharePoint + Blob Storage?
   - **Public container** (anonymous read) or **Private** (SAS URLs)?

---

## Comparison: SharePoint vs Blob Storage

| Feature | SharePoint (Current) | Blob Storage |
|---------|---------------------|--------------|
| **Team Access** | ✅ Better (Office UI) | ⚪ Via URL only |
| **Cost** | ✅ Free (part of O365) | ✅ Very cheap |
| **Setup Complexity** | ⚪ Power Automate needed | ✅ Simple SDK |
| **Reliability** | ⚪ Webhook dependency | ✅ Direct API |
| **Overwrite** | ✅ Yes | ✅ Yes |
| **Versioning** | ✅ Native | ✅ Optional |
| **Download Speed** | ⚪ Slower | ✅ Fast CDN |

**Recommendation:** Use **both**
- SharePoint for team collaboration
- Blob Storage as reliable backup/archive
