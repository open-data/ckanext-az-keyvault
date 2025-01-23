[![Tests](https://github.com/open-data/ckanext-az-keyvault/workflows/Tests/badge.svg?branch=main)](https://github.com/open-data/ckanext-az-keyvault/actions)

# ckanext-az-keyvault

CKAN Extentsion for Azure Key Vault itegration. This plugin provides the ability to store CKAN config option values in an Azure Key Vault.


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | Not tested    |
| 2.7             | Not tested    |
| 2.8             | Not tested    |
| 2.9             | Yes    |
| 2.10            | Yes    |

| Python version    | Compatible?   |
| --------------- | ------------- |
| 2.9 and earlier | No    |
| 3.0 and later             | Yes    |

## Installation

To install ckanext-az-keyvault:

1. Activate your CKAN virtual environment, for example:

     `. /usr/lib/ckan/default/bin/activate`

2. Clone the source and install it on the virtualenv

    - `git clone --branch main --single-branch https://github.com/open-data/ckanext-az-keyvault.git`
    - `cd ckanext-az-keyvault`
    - `pip install -e .`
    - `pip install -r requirements.txt`

3. Add `az_keyvault` to the `ckan.plugins` setting in your CKAN
   config file. Make sure to add it to the **top** so that the config values are
   pulled from Azure Key Vault for the other plugins to use.

4. Restart CKAN

## Config settings

- The Azure Key Vault Name (the `KEY_VAULT_NAME` environment variable).

  *Required:* `True`

  *Default:* `None`

  ```
  ckanext.az_keyvault.vault_name = <Azure Key Vault Name>
  ```
- Azure Key Vault period character.

  *Required:* `False`

  *Default:* `#`

  ```
  ckanext.az_keyvault.period_char = ^
  ```

## Storing CKAN Options in Key Vault

To have a CKAN config options stored in the Key Vault, create the key value pair in the Azure Key Vault with the name of the CKAN config option the same, with the following caveat: periods are not allowed in Azure Key Vault key names. Thus, replace any periods in the CKAN config option name with `#` (controllable with `ckanext.az_keyvault.period_char`, see above).

In the CKAN config file, set the value to the stored key to `AZURE_KEY_VAULTED`, this plugin will then attempt to go fetch the stored value from the Azure Key Vault.


## MSI Configuration

This plugin uses `ManagedIdentityCredential (MSI)` on a system level to authenticate with Azure.

See: https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/qs-configure-portal-windows-vm

See: https://pypi.org/project/azure-identity/ (section: Authenticate with a system-assigned managed identity)

## License

[MIT](https://raw.githubusercontent.com/open-data/ckanext-az-keyvault/main/LICENSE)
