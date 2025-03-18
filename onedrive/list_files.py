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
    
    print(f"\nFiles in {folder_path or 'root folder'}:")
    print("-" * 50)
    
    for item in items:
        item_type = "Folder" if item.is_folder else "File"
        print(f"{item_type}: {item.name}")
        
        # If you want to include file details:
        if not item.is_folder:
            print(f"  - Size: {item.size} bytes")
            print(f"  - URL: {item.web_url}")
            print(f"  - Last modified: {item.modified}")
        print("-" * 50)

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

if __name__ == "__main__":
    # Example usage
    # list_onedrive_files()
    list_onedrive_files('JobAssist/voice_memos')
    
    # Uncomment to list files in a specific folder
    # list_onedrive_files('Documents/Work')
    
    # Uncomment to download a specific file
    # download_file('Documents/report.docx', 'downloaded_report.docx')
