"""
TODO: DEPRECATE. Future apps should simply use boto/3 directly, this doesn't add
anything.
"""

import logging
from boto3.session import Session

logger = logging.getLogger(__name__)


class S3Connector(object):
    """ Methods to interact with an S3 bucket

    Args:
        aws_access_key_id: The AWS ACCESS KEY ID
        aws_secret_access_key: The AWS SECRET ACCESS KEY
        aws_region: The AWS region. Defaults to `us-east-1`
    """
    def __init__(self, aws_access_key_id, aws_secret_access_key,
                 aws_region='us-east-1'):
        session = Session(aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=aws_region)
        self.client = session.client('s3')

    def list_objects(self, bucket, folder=''):
        """ List the objects in a specific bucket and optionally folder.

            This strips out the metadata that is sent along with the
            list_objects() method and returns only the Contents list.

        Args:
            bucket: The S3 bucket
            folder: A folder within a bucket. Defaults to empty string.
        """
        try:
            retval = self.client.list_objects(
                Bucket=bucket,
                Delimiter='/',
                Prefix=folder
            )
        except Exception as e:
            logger.exception(e)
            return None

        if 'Contents' not in retval.keys():
            return None

        return retval['Contents']

    def put(self, bucket, key, body, metadata={}):
        """ Put an object into a specific bucket with a key

        Args:
            bucket: The S3 bucket
            key: The object's `key`
            body: The object's `body`
            metadata: Any metadata to associate with the object.
        """
        try:
            self.client.put_object(
                Bucket=bucket,
                Key=key,
                Body=body,
                Metadata=metadata
            )
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def upload_file(self, bucket, key, file_path):
        """ Uploads a local file to a S3 bucket. It performs multipart uploads
        for large files.

        Args:
            bucket: The S3 bucket
            key: The object's `key`
            file_path: Location of the file to upload

        Retruns: True if the file was uploaded, False otherwise.
        """

        try:
            self.client.upload_file(
                Filename=file_path,
                Bucket=bucket,
                Key=key
            )
        except Exception as e:
            logger.exception(e)
            return False

        return True

    def get(self, bucket, key):
        """ Retrieve a specific key's value from a bucket

        Args:
            bucket: The S3 bucket
            key: The object's `key`
        """
        try:
            return self.client.get_object(
                Bucket=bucket,
                Key=key
            )
        except Exception as e:
            logger.exception(e)
            return None

    def get_meta(self, bucket, key):
        """ Retrieve a specific key's meta data from a bucket

        Args:
            bucket: The S3 bucket
            key: The object's `key`
        """
        try:
            return self.client.head_object(
                Bucket=bucket,
                Key=key
            )
        except Exception as e:
            logger.exception(e)
            return None

    def copy_object(self, src_bucket, src_key, metadata=None,
                    dest_bucket=None, dest_key=None):
        """ Copy an object. If no destination bucket/key provided, then update.

            Allows optional update to object's meta data.

        Args:
            src_bucket: The S3 source bucket from which to copy.
            src_key: The key of the object to copy.
            metadata: Any new metadata for the object.
            dest_bucket: The destination bucket. If None, the source bucket is
                used instead.
            dest_key: The key of the destination object. If None, the source
                key is used instead.
        """
        metadata_directive = 'COPY' if metadata is None else 'REPLACE'
        metadata = {} if metadata is None else metadata

        if dest_bucket is None:
            dest_bucket = src_bucket

        if dest_key is None:
            dest_key = src_key

        try:
            return self.client.copy_object(
                Bucket=dest_bucket,
                Key=dest_key,
                Metadata=metadata,
                MetadataDirective=metadata_directive,
                CopySource=src_bucket + "/" + src_key
            )
        except Exception as e:
            logger.exception(e)
            return None

    def delete(self, bucket, key):
        """ Delete a specific key

        Args:
            bucket: The S3 bucket
            key: The object's `key`
        """
        try:
            return self.client.delete_object(
                Bucket=bucket,
                Key=key
            )
        except Exception as e:
            logger.exception(e)
            return None

    def delete_multiple(self, bucket, keys):
        """ Delete a set of keys. Expects an array of objects with 'Key' key

        Args:
            bucket: The S3 bucket
            keys: The list of keys
        """
        try:
            return self.client.delete_objects(
                Bucket=bucket,
                Delete={
                    'Objects': keys
                }
            )
        except Exception as e:
            logger.exception(e)
            return None
