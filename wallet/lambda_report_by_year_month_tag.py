import json
import os

import boto3

import aws_utils
import money_operations_reports


def lambda_handler(event, context):
    money_operations_file = aws_utils.get_file_name_with_money_operations(event)

    # loads money operations from json
    money_operations = aws_utils.load_money_operations_from_json(
        money_operations_file["bucket"],
        money_operations_file["key"],
        boto3.client("s3")
    )

    # creates money operations report as dictionary
    money_operations_report = money_operations_reports.group_by_year_month_tag(money_operations)

    aws_utils.save_to_s3(
        money_operations_report,
        os.getenv("reports_bucket"),
        os.getenv("report_key"),
        boto3.client("s3")
    )

