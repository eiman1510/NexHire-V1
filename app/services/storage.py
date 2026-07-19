from core.config import BUCKET_NAME, s3
from uuid import uuid4


def upload_resume(file, candidate_id):

    extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid4()}.{extension}"
    key = f"resumes/{candidate_id}/{unique_filename}"

    s3.upload_fileobj(
        file.file, BUCKET_NAME, key, ExtraArgs={"ContentType": file.content_type}
    )

    return key


def get_file_url(key):

    url = s3.generate_presigned_url(
        "get_object", Params={"Bucket": BUCKET_NAME, "Key": key}, ExpiresIn=3600
    )

    return url


def delete_file(key):

    s3.delete_object(Bucket=BUCKET_NAME, Key=key)
