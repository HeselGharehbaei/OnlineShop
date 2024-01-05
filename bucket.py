import boto3
from django.conf import settings
from botocore.exceptions import ClientError
import logging


class Bucket:
    """
    CND bucket manager

    init method creates connection.

    NOTE:
        none of thise methods are async. use public interface in tasks.py modules instead.
    """

    def __init__(self):
        self.conn= boto3.client(
            service_name= settings.AWS_SERVICE_NAME,
            aws_access_key_id= settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url= settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        result= self.conn.list_objects_v2(Bucket= settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        else:
            return None    

    def delete_object(self, key):
        try:
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            self.conn.delete_object(Bucket= bucket_name, Key= key)
            return True
        except ClientError as e:
            logging.error(e)    


    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f:
            self.conn.download_fileobj( settings.AWS_STORAGE_BUCKET_NAME, key, f) 
            return True  

    def upload_object(self):
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        with open(settings.AWS_LOCAL_STORAGE + '/Hawaii.png', "rb") as f:
            self.conn.upload_fileobj(f, bucket_name, 'Hawaii.png')
        return True 
            

bucket = Bucket()        
