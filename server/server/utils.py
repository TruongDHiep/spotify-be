import boto3
from django.conf import settings
from urllib.parse import urlparse
from boto3.s3.transfer import TransferConfig
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

def delete_from_s3(url):
    # Loại bỏ phần timestate (?t=timestamp)
    parsed_url = urlparse(url)
    file_path = parsed_url.path.lstrip('/')  # bỏ dấu '/' đầu tiên nếu có

    # Khởi tạo client S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    # Xóa file khỏi bucket
    s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_path)