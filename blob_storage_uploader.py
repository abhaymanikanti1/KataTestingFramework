"""
Azure Blob Storage Upload Module
Uploads Excel files to Azure Blob Storage and provides download functionality for API server
"""
from azure.storage.blob import BlobServiceClient
import os
from datetime import datetime

# Configuration
CONTAINER_NAME = 'kata-reports'
BLOB_NAME = 'degraded_responses.xlsx'  # Fixed filename - overwrites existing

def _get_connection_string():
    """Get connection string from environment variable"""
    conn_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    if not conn_str:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set")
    return conn_str

def upload_excel_to_blob(local_file_path, blob_name=BLOB_NAME):
    """
    Upload Excel file to Azure Blob Storage
    - Overwrites existing file with same name
    - Returns blob URL
    
    Args:
        local_file_path: Path to local Excel file
        blob_name: Name for the blob (default: degraded_responses.xlsx)
    
    Returns:
        str: Blob URL if successful, None if failed
    """
    try:
        connection_string = _get_connection_string()
    except ValueError as e:
        print(f"\n  ⚠️  {e}")
        print("  Set it with: export AZURE_STORAGE_CONNECTION_STRING='your-connection-string'")
        return None
    
    if not os.path.exists(local_file_path):
        print(f"\n  ⚠️  File not found: {local_file_path}")
        return None
    
    try:
        print(f"\n  📤 Uploading {os.path.basename(local_file_path)} to Azure Blob Storage...")
        
        # Create clients
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_client = container_client.get_blob_client(blob_name)
        
        # Upload file (overwrite if exists)
        with open(local_file_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        
        blob_url = blob_client.url
        file_size = os.path.getsize(local_file_path)
        
        print(f"  ✅ Upload successful!")
        print(f"  📁 File size: {file_size:,} bytes")
        print(f"  📦 Container: {CONTAINER_NAME}")
        print(f"  📄 Blob name: {blob_name}")
        print(f"  🔗 Blob URL: {blob_url}")
        
        return blob_url
        
    except Exception as e:
        print(f"\n  ❌ Error uploading to Blob Storage: {e}")
        import traceback
        traceback.print_exc()
        return None

def download_excel_from_blob(blob_name=BLOB_NAME, local_file_path=None):
    """
    Download Excel file from Azure Blob Storage
    Used by API server to read latest data
    
    Args:
        blob_name: Name of the blob to download
        local_file_path: Local path to save file (default: /tmp/blob_name)
    
    Returns:
        str: Path to downloaded file if successful, None if failed
    """
    connection_string = _get_connection_string()
    
    if local_file_path is None:
        local_file_path = f"/tmp/{blob_name}"
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(CONTAINER_NAME, blob_name)
        
        # Download blob to file
        with open(local_file_path, 'wb') as download_file:
            download_file.write(blob_client.download_blob().readall())
        
        print(f"  📥 Downloaded {blob_name} to {local_file_path}")
        return local_file_path
        
    except Exception as e:
        print(f"  ❌ Error downloading from Blob Storage: {e}")
        return None

def check_blob_exists(blob_name=BLOB_NAME):
    """
    Check if blob exists in storage
    
    Returns:
        bool: True if blob exists, False otherwise
    """
    try:
        connection_string = _get_connection_string()
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(CONTAINER_NAME, blob_name)
        return blob_client.exists()
    except:
        return False

def get_blob_metadata(blob_name=BLOB_NAME):
    """
    Get metadata about the blob (size, last modified, etc.)
    
    Returns:
        dict: Metadata dictionary or None if failed
    """
    try:
        connection_string = _get_connection_string()
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(CONTAINER_NAME, blob_name)
        
        if not blob_client.exists():
            return None
        
        properties = blob_client.get_blob_properties()
        
        return {
            'name': blob_name,
            'size': properties.size,
            'last_modified': properties.last_modified,
            'content_type': properties.content_settings.content_type,
            'url': blob_client.url
        }
    except Exception as e:
        print(f"Error getting blob metadata: {e}")
        return None

# Test the upload when run directly
if __name__ == "__main__":
    print("="*70)
    print("🧪 Testing Azure Blob Storage Upload")
    print("="*70)
    
    test_file = "Degraded_Responses_Report.xlsx"
    
    if os.path.exists(test_file):
        print(f"Found test file: {test_file}")
        url = upload_excel_to_blob(test_file)
        
        if url:
            print(f"\n{'='*70}")
            print("✅ SUCCESS! File uploaded to Azure Blob Storage")
            print(f"{'='*70}")
            print(f"🔗 URL: {url}")
            
            # Show metadata
            metadata = get_blob_metadata()
            if metadata:
                print(f"\n📊 Blob Metadata:")
                print(f"   Size: {metadata['size']:,} bytes")
                print(f"   Last Modified: {metadata['last_modified']}")
                print(f"   Content Type: {metadata['content_type']}")
        else:
            print(f"\n{'='*70}")
            print("❌ Upload failed - check error messages above")
            print(f"{'='*70}")
    else:
        print(f"\n❌ Test file not found: {test_file}")
        print("\nTo create a test file, run:")
        print("  python integrated_test_comparison.py")
        print("\nThis will generate the degraded responses report.")
