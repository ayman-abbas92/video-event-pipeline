import boto3
import os
import sys


def upload_to_s3(bucket_name, file_path, s3_key):
    """
    Upload a file to an S3 bucket.

    :param bucket_name: Name of the S3 bucket
    :param file_path: Path to the file to upload
    :param s3_key: S3 key (path) where the file will be stored
    """
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"File {file_path} uploaded to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python upload_to_s3.py <bucket_name> <file_path> <s3_key>")
        sys.exit(1)

    bucket_name = sys.argv[1]
    file_path = sys.argv[2]
    s3_key = sys.argv[3]

    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        sys.exit(1)

    upload_to_s3(bucket_name, file_path, s3_key)