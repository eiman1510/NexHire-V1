from core.config import BUCKET_NAME, s3_client
from uuid import uuid4

#gets a pdf and save it in the destined s3 bucket and return the pdf key
def upload_resume(file, candidate_id):

    extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid4()}.{extension}" #why uuid4? many candidate may have resume saved as resume.pdf or cv.pdf so add random combo after to make it unique
    key = f"resumes/{candidate_id}/{unique_filename}"

    s3_client.upload_fileobj(
        file.file, BUCKET_NAME, key, ExtraArgs={"ContentType": file.content_type}
    )

    return key

#this return the presigned url
'''
a presigned url allow seeing/accessing a private document for the time assigned 
in this the url will give access for one hour 
'''
def get_file_url(key):

    url = s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": BUCKET_NAME, "Key": key}, ExpiresIn=3600
    )

    return url

#delete file from s3
def delete_file(key):

    s3_client.delete_object(Bucket=BUCKET_NAME, Key=key)
