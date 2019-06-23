import boto3


def read_all_lines_froms3key(s3_bucket: str, s3_key_obj: str) -> str:
    s3 = boto3.resource('s3')
    s3_object = s3.Object(s3_bucket, s3_key_obj)
    obj_details = s3_object.get()
    return obj_details['Body'].read()