import boto3


def read_all_lines_froms3key(s3_bucket: str, s3_key_obj: str) -> str:
    s3 = boto3.resource('s3')
    s3_object = s3.Object(s3_bucket, s3_key_obj)
    obj_details = s3_object.get()
    return obj_details['Body'].read().decode("utf-8")


def get_file_name_with_money_operations(s3_trigger_lambda_event):
    """
    Returns dictionary with "bucket" and "key" properties as a result
    :param s3_trigger_lambda_event: object passed to the lambda handler
    :return: dictionary
    """
    return {
        "bucket": s3_trigger_lambda_event['Records'][0]['s3']['bucket']['name'],
        "key": s3_trigger_lambda_event['Records'][0]['s3']['object']['key']
    }