# Installation
************
pip install crio_vault


# Get started
***********

# How to fetch keys required by a script from the AWS secret manager vault with this lib:

from crio_vault import vault

# Instantiate
fetch = vault()

# Call the fetch_and_store method
fetch.fetch_and_store("test100", "prod")
key = json.loads(os.getenv('TEST100_PROD_SHEET_KEY')) # dict
token = os.getenv('TEST100_PROD_TOKEN') # string 

# Print and check 
print(key)
print(type(key))
print(token)
print(type(token))