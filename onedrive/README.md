# OneDrive Integration

This module provides functionality to connect to OneDrive and retrieve files using the python-o365 library.

## Setup

1. Install the required dependencies:
   ```
   pip install O365
   ```

2. Register an application in the Azure portal:
   - Go to Azure Active Directory > App registrations > New registration
   - Name your application
   - For redirect URI:
     - Select "Web" as the platform
     - Set redirect URI to `https://login.microsoftonline.com/common/oauth2/nativeclient`
     - You can also add `http://localhost:8000` as an alternative
   - Under "API Permissions", add Microsoft Graph permissions: `Files.Read`, `Files.ReadWrite`
   - Create a client secret under "Certificates & secrets"

3. Create a `.env` file with your app details:
```
ONEDRIVE_APP_CLIENT_ID=""
ONEDRIVE_APP_CLIENT_SECRET=""
AZURE_STORAGE_CONNECTION_STRING=""
AZURE_STORAGE_CONTAINER_NAME=""
```

## Usage

Run the `list_files.py` script to authenticate and list files from your OneDrive:
