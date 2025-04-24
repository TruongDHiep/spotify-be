import boto3
from django.conf import settings
import uuid

def upload_to_s3(file, folder):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    ext = file.name.split('.')[-1]
    filename = f"{folder}/{uuid.uuid4()}.{ext}"

    s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, filename)
    url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
    return url
