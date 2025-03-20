import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

def vault_get_secret(secret_name):
    load_dotenv()
    key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
    key_vault_creds = DefaultAzureCredential()
    key_vault_client = SecretClient(vault_url=key_vault_uri, credential=key_vault_creds)    
    secret = key_vault_client.get_secret(secret_name)
    return secret.value
def vault_set_secret(secret_name, secret_value):
    load_dotenv()
    key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
    key_vault_creds = DefaultAzureCredential()
    key_vault_client = SecretClient(vault_url=key_vault_uri, credential=key_vault_creds)
    key_vault_client.set_secret(secret_name, secret_value)

if __name__ == "__main__":
    pass