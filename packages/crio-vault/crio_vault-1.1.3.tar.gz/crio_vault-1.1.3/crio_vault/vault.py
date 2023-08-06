# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:   
# https://aws.amazon.com/developers/getting-started/python/


from asyncio.log import logger
import boto3
import base64
from botocore.exceptions import ClientError
import json
import os
import os.path
from requests import session
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#CRIO_ESSENTIAL_VAULT_KEY_NAME="crio/env" =? env => prod, dev
#REPO_SPECIFIC_VAULT_NAME="repo_name/env" => env => prod, dev, local 

REGION_NAME = "ap-south-1"
AWS_ACCESS_KEY_ID = os.environ['VAULT_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['VAULT_AWS_SECRET_ACCESS_KEY']
SERVICE_NAME = 'secretsmanager'
CRIO = 'crio'


class vault(object):

    # Creates a session manager client
    def __init__(self):
        session = boto3.session.Session()
        self.client = session.client(
            service_name=SERVICE_NAME,
            region_name=REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )



    # Fetch the secrets from the vault
    def get_secret(self, env, repo_name):
        # write the secret name as stored in the vault
        secret_name = (repo_name + "/" + env)

        if(repo_name == CRIO):
            secret_name = (repo_name + "/" + env)

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
            logging.info("Secrets fetched from " + secret_name + "...")
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
        else:
            # Decrypts secret using the associated KMS key.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

        # Return the fetched secret    
        return get_secret_value_response



    # Delete a secret 
    def delete_secret(self, repo_name, env):
        secret_name = (repo_name + "/" + env)
        response = self.client.delete_secret(
            RecoveryWindowInDays=7,
            SecretId=secret_name,
        )



    # Parse and stores the secrets as environment variable
    def parse_and_store_env(self, secret, env, repo_name):
        # Iterating the dictionary secret
        for a, b in secret.items():
            if a == "SecretString":
                res = json.loads(b)
                for key, value in res.items():
                    # dictionary[key] = value
                    # name = SESSION_MANAGEMENT_PROD_<name_of_secret_file> 
                    name = "{}_{}_{}".format(repo_name.upper(), env.upper(), key.upper())
                    if type(value) != type(a):
                        val = json.dumps(value)
                        os.environ[name] = val
                    else:
                        os.environ[name] = value
    


    # Fetch the keys from the vault and store it in environment variable
    def fetch_and_store(self, repo_name, env):
        # Store all keys in environment variables
        secret_repo = self.get_secret(env, repo_name)
        self.parse_and_store_env(secret_repo, env, repo_name)


#************************#
def main():
    pass

if __name__=="__main__":
    main()






