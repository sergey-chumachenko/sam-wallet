import json
from typing import Any
from typing import Dict
from typing import Sequence

import jsondatetime


def read_all_lines_froms3key(s3_bucket: str, s3_key_obj: str, s3_client) -> str:
    obj_details = s3_client.get_object(Bucket=s3_bucket, Key=s3_key_obj)
    return obj_details['Body'].read().decode("utf-8")


def get_file_name_with_money_operations(s3_trigger_lambda_event) -> Dict[str,str]:
    """
    Returns dictionary with "bucket" and "key" properties as a result
    :param s3_trigger_lambda_event: object passed to the lambda handler
    :return: dictionary
    """
    return {
        "bucket": s3_trigger_lambda_event['Records'][0]['s3']['bucket']['name'],
        "key": s3_trigger_lambda_event['Records'][0]['s3']['object']['key']
    }


def save_to_s3(obj_content: Any, dest_s3_bucket: str, dest_s3_obj_key: str, s3_client):
    return s3_client.put_object(
        Bucket=dest_s3_bucket,
        Key=dest_s3_obj_key,
        Body=json.dumps(obj_content, default=str)
    )


def load_money_operations_from_json(dest_s3_bucket: str, dest_s3_obj_key: str, s3_client) -> Sequence[Dict[str,Any]]:
    """
    Loads money operations stored as list of objects in JSON-format and returns Python's objects.
    Converts values with date to python's date object
    :param dest_s3_bucket: s3 bucket where object is stored
    :param dest_s3_obj_key: s3 key to object with money operations
    :param s3_client: service used to read data from s3 bucket
    :return: Python's dictionary
    """
    file_content = read_all_lines_froms3key(dest_s3_bucket, dest_s3_obj_key, s3_client)
    money_operations = json.loads(file_content)

    # converts all values with date to datetime.date
    for money_op in money_operations:
        jsondatetime.iteritems(money_op)
        money_op["date"] = money_op["date"].date()

    return money_operations

