# pylint: disable=too-few-public-methods

"""
    CUSTOM WRITER CLASSES
"""
import os
import json
from datetime import datetime
import boto3

class CustomS3JsonWriter:
    """Class to write files to s3"""
    data = None
    def __init__(self, bucket: str, profile_name: str=None) -> None:
        self.bucket = bucket
        self.profile_name = profile_name

        if profile_name is None:
            self.boto3_session = boto3.Session()
        else:
            self.boto3_session = boto3.Session(profile_name=profile_name)

        self.s3_resource = self.boto3_session.resource("s3")

    def write_to_s3(self, json_data: json, config: dict):
        """
        Construct partitioning and file name conventions in s3
        according to business specifications, and write to S3.
        """
        data_variant = config.get("data_variant").lower()
        collection_name = config.get("collection_name").lower()
        organisation_name = config.get("tenant_name").lower()
        if not ( data_variant and collection_name and organisation_name and json_data ):
            raise ValueError(
                'One or more required attributes ("data_variant", "collection_name", "tenant_name") missing from request config'
            )
        
        _date = config.get( "date", datetime.now().strftime("%Y-%m-%d") ).replace("-", "")

        key_path = f"{data_variant}/{organisation_name}/{collection_name}/{_date}.json"
        # replace any '-' in the path, just in case; we don't want s3 to panic
        key_path = "_".join( key_path.split("-") )

        print( f"Write path: S3://{self.bucket}/{key_path}" )
        self.data = json_data
        self.s3_resource.Object(self.bucket, key_path).put( Body = json.dumps( json_data ) )
