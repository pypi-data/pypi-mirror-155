import os
from functools import lru_cache
from logging import getLogger

from azure.core.exceptions import ClientAuthenticationError, ResourceNotFoundError
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

from .exceptions import AuthenticationError, SecretNotFoundError

__all__ = ["get_secret", "sanitize_secret_name"]
logger = getLogger(__name__)

NOT_FOUND = "not-found"  # must be a string for Azure SDK
TENANT_ID = os.environ.get("KV_KEYPRHSTREAMLITDADEV_AZURETENANTID", NOT_FOUND)
CLIENT_ID = os.environ.get("KV_KEYPRHSTREAMLITDADEV_AZURECLIENTID", NOT_FOUND)
CLIENT_SECRET = os.environ.get("KV_KEYPRHSTREAMLITDADEV_AZURECLIENTSECRET", NOT_FOUND)
KEY_VAULT_NAME = os.environ.get("AZURE_KEY_VAULT_NAME", "keyprhsandboxdev")
KEY_VAULT_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net/"

if any(ev == NOT_FOUND for ev in (TENANT_ID, CLIENT_ID, CLIENT_SECRET)):
    logger.warning(
        "Azure KeyVault credentials not found in environment variables. "
        "Secrets lookup will fail."
    )


def build_secrets_getter():
    """Return a callable that wrapps Azure KeyVault 'get_secret' method."""
    credentials = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    client = SecretClient(KEY_VAULT_URL, credentials)

    def get(name):
        logger.debug(f"Fetching '{name}' from KeyVault...")
        try:
            secret = client.get_secret(name)
        except ClientAuthenticationError as e:
            raise AuthenticationError(
                f"Failed to authenticate on KeyVault '{KEY_VAULT_URL}'.\n"
                "Check the following environment variables: 'AZURE_TENANT_ID',"
                "'AZURE_CLIENT_ID', 'AZURE_CLIENT_SECRET', 'AZURE_KEY_VAULT_NAME'"
            ) from e
        except ResourceNotFoundError as e:
            raise SecretNotFoundError(
                f"Secret '{name}' not found in Azure KeyVault '{KEY_VAULT_URL}'."
            ) from e
        else:
            return secret.value

    return get


# The low-level action requires a network call. We use memoization to optimize
# for speed.
get_secret = lru_cache(build_secrets_getter())
