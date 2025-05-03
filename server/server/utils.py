import boto3
from django.conf import settings
from urllib.parse import urlparse
from boto3.s3.transfer import TransferConfig
import uuid

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)


def upload_to_s3(file, folder):
    ext = file.name.split('.')[-1]
    filename = f"{folder}/{uuid.uuid4()}.{ext}"

    config = TransferConfig(
        multipart_threshold=5 * 1024 * 1024,  # Tự động dùng multipart nếu file >5MB
        max_concurrency=5,  # Số thread đồng thời
        multipart_chunksize=5 * 1024 * 1024,
        use_threads=True
    )

    try:
        s3_client.upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            filename,
            Config=config,
            ExtraArgs={'ContentType': file.content_type}
        )
    except Exception as e:
        raise RuntimeError(f"Upload failed: {str(e)}")

    return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"

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