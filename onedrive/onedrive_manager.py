from O365 import Account, FileSystemTokenBackend
import os
import yaml
import sys
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("ONEDRIVE_APP_CLIENT_ID")
CLIENT_SECRET = os.getenv("ONEDRIVE_APP_CLIENT_SECRET")

def authenticate():
    """Authenticate with Microsoft Graph API"""
    
    # Setup token backend to store authentication tokens
    token_backend = FileSystemTokenBackend(token_path='.', token_filename='.o365_token.txt')
    
    # Initialize account with credentials
    account = Account((CLIENT_ID, CLIENT_SECRET), 
                      auth_flow_type='authorization',
                      token_backend=token_backend)
    
    # Request authentication
    if not account.is_authenticated:
        # Use browser based authentication
        # The redirect_uri here should match what you set in the Azure portal
        if account.authenticate(scopes=['files.read', 'files.readwrite'],
                               redirect_uri='https://login.microsoftonline.com/common/oauth2/nativeclient'):
            print('Authentication successful')
        else:
            print('Authentication failed. Please check your client_id, client_secret, and redirect_uri configuration.')
            return None
    else:
        print('Already authenticated')
    
    return account

def list_onedrive_files(folder_path=None):
    """List files in OneDrive, optionally from a specific folder"""
    account = authenticate()
    if not account:
        return
    
    # Get the OneDrive storage
    storage = account.storage()
    drive = storage.get_default_drive()
    
    # Get root folder or specified folder
    if folder_path:
        folder = drive.get_item_by_path(folder_path)
    else:
        folder = drive.get_root_folder()
    
    # List items in the folder
    items = folder.get_items()
    return items

def download_file(file_path, save_path):
    """Download a specific file from OneDrive"""
    account = authenticate()
    if not account:
        return
    
    storage = account.storage()
    drive = storage.get_default_drive()
    
    # Get the file
    file = drive.get_item_by_path(file_path)
    
    # Download the file
    if file:
        file.download(save_path)
        print(f"File downloaded to {save_path}")
    else:
        print(f"File not found: {file_path}")

def copy_file_to_blob_storage(onedrive_path, blob_path):
    """Copy a file from OneDrive to Azure Blob Storage"""
    account = authenticate()
    if not account:
        return
    
    storage = account.storage()
    drive = storage.get_default_drive()
    
    # Get the file
    file = drive.get_item_by_path(onedrive_path)
    
    # Download the file
    if file:
        # Save the file to a temporary location
        temp_path = './tmp'
        file.download(temp_path)
        
        local_file = os.path.join(temp_path, file.name)
        # Upload the file to Azure Blob Storage
        upload_blob_from_file(local_file, blob_path)
        print(f"File copied to Azure Blob Storage: {blob_path}")
    else:
        print(f"File not found: {onedrive_path}")

def upload_blob_from_file(file_path, blob_path):
    """Upload a file to Azure Blob Storage"""
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
    import os
    
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
    
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)
    
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

if __name__ == "__main__":
    # Example usage
    # list_onedrive_files()
    onedrive_voice_memo_path = 'JobAssist/voice_memos'
    voice_memos_to_sync = list_onedrive_files(onedrive_voice_memo_path)
    for voice_memo in voice_memos_to_sync:
        onedrive_path = f"{onedrive_voice_memo_path}/{voice_memo.name}"
        blob_path = f"voice_memos/{voice_memo.name}"
        print(f"Copying {onedrive_path} to {blob_path}")
        copy_file_to_blob_storage(onedrive_path, blob_path)
    
    # Uncomment to list files in a specific folder
    # list_onedrive_files('Documents/Work')
    
    # Uncomment to download a specific file
    # download_file('Documents/report.docx', 'downloaded_report.docx')
