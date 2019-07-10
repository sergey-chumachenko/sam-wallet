"""
Groups money operations by year, month and tag from json-file and puts report to s3 bucket as a json-file.
The source with money operations is specified by money_op_s3_bucket and money_op_s3_obj_key environment variales
The destination for the report is specified in report_s3_bucket and report_s3_obj_key
"""
import json
import os

import boto3

import aws_utils
import money_operations_reports


def lambda_handler(event, context):
    # loads money operations from json
    money_operations = aws_utils.load_money_operations_from_json(
        os.environ["money_op_s3_bucket"],
        os.environ["money_op_s3_obj_key"],
        boto3.client("s3")
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            money_operations_reports.group_by_year_month_tag(money_operations)
        )
    }
