from ckan.common import CKANConfig

from logging import getLogger
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

import ckan.plugins as plugins


log = getLogger(__name__)


@plugins.toolkit.blanket.config_declarations
class AzureKeyVaultPlugin(plugins.SingletonPlugin):
    """
    Integrate Azure Key Vault python library to store CKAN config option values.
    """
    plugins.implements(plugins.IConfigurer, inherit=True)

    # IConfigurer
    def update_config(self, config: 'CKANConfig'):
        key_vault_name = config.get('ckanext.az_keyvault.vault_name')
        if not key_vault_name:
            raise Exception('ckanext.az_keyvault.vault_name is not '
                            'defined but is required by the az_keyvault plugin.')

        azure_keys = []
        for key, value in config.items():
            if value != 'AZURE_KEY_VAULTED':
                continue
            azure_keys.append(key)

        if not azure_keys:
            log.debug('No AZURE_KEY_VAULTED config options...')
            return

        period_replace_char = config.get('ckanext.az_keyvault.period_char', '#')
        key_vault_uri = f"https://{key_vault_name}.vault.azure.net"

        try:
            credential = ManagedIdentityCredential()
        except ValueError:
            raise Exception("An Azure Client ID has not been configured.")

        client = SecretClient(vault_url=key_vault_uri,
                              credential=credential)

        for key in azure_keys:
            az_key = key.replace('.', period_replace_char)
            az_value = client.get_secret(az_key)
            if az_value:
                config[key] = az_value
