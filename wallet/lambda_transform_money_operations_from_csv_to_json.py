"""
This lambda is triggered by S3 events.
It transforms money operations from csv-file to json and saves to the object.
The S3 bucket and object key destination are specified in the following environment variables:
dest_s3_bucket and dest_s3_obj_key
"""
import os

import boto3

import aws_utils
import money_operation_utils
from money_operation_utils import save_to_s3


def lambda_handler(event, _context):
    # gets name of the file with money operations
    file_name = aws_utils.get_file_name_with_money_operations(event)

    # reads money operations from file
    all_money_op_as_csv = aws_utils.read_all_lines_froms3key(file_name["bucket"], file_name["key"])
    money_operations = money_operation_utils.read_money_operations_from_csv(all_money_op_as_csv)

    s3_client = boto3.client("s3")
    return save_to_s3(
        money_operations,
        os.environ["dest_s3_bucket"],
        os.environ["dest_s3_obj_key"],
        s3_client
    )


