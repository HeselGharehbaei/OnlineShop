from bucket import bucket
from celery import shared_task


# TODO: can be async?
def all_bucket_objects_task():
    result= bucket.get_objects()
    return result 
