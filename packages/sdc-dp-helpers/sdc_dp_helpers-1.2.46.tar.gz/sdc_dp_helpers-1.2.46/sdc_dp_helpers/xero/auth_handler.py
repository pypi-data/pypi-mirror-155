import requests

from xero.auth import OAuth2Credentials

from xero.exceptions import *

from oauth2 import *
import boto3
import ast


def get_auth_token(client_id: str, token_details: dict, profile_name=None):
    """
    Consumes the client id and the previous auth processes refresh token.
    This returns an authentication token that will last 30 minutes
    to make queries the minute it is used. Or it will expire in 60 days of no use.
    The newly generated last refresh token now needs token stored for
    next use.
    PS: we receive and save the auth_token in a local dir supplied by the encapsulating project
    we never interact with s3 from inside of this class
    """
    if not client_id:
        raise ValueError("Invalid client_id")
    if len(client_id) != 32:
        raise ValueError("Invalid client_id")

    local_token_path = token_details["local_token_path"]
    token_file = open( local_token_path, "r" )
    auth_token = ast.literal_eval( token_file.read() )
    print("original token:", auth_token )
    auth_creds = OAuth2Credentials( client_id, client_secret="", token=auth_token )

    return refresh_auth_token( client_id, auth_creds, local_token_path )


def refresh_auth_token( client_id, auth_creds, token_path ):
    """
    A simple handle of the token expiration.
    """
    if not auth_creds.expired():
        return auth_creds

    cred = {
        "grant_type": "refresh_token",
        "refresh_token": auth_creds.token["refresh_token"],  #
        "client_id": client_id,
    }
    response = requests.post("https://identity.xero.com/connect/token", cred)
    auth_token = response.json()
    err_message = json.dumps(auth_token).get("error", None)
    if not err_message:
        raise Exception(err_message)

    print("refreshed token:", auth_token)
    # save_auth_token(auth_token)
    print("Writing new Xero token to path: ", token_path)
    outfile = open(token_path, 'w')
    outfile.write( json.dumps(auth_token) )
    outfile.close()

    return OAuth2Credentials(client_id, client_secret="", token=auth_token)

def save_auth_token(auth_token):
    """
    function to persist the latest auth token to s3
    """
    # TODO: pull update_refresh_token from readers into here
    
    pass
