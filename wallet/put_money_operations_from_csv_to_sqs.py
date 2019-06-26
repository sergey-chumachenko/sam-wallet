"""
It is triggered by S3 object create event. The event contains s3key of the money operations sources.
Transforms money operation from comma separated to dictionary and puts it to SQS.
The name of queue in SQS is specified in money_operations_sqs_queue environment variable
"""
import json
import os
from typing import Any
from typing import Dict
from typing import Sequence

import boto3

import aws_utils
import money_operation_utils


def lambda_handler(event, _context):
    # gets name of the file with money operations
    file_name = aws_utils.get_file_name_with_money_operations(event)

    # reads money operations from file
    all_money_op_as_csv = aws_utils.read_all_lines_froms3key(file_name["bucket"], file_name["key"])
    money_operations = money_operation_utils.read_money_operations_from_csv(all_money_op_as_csv)

    # puts money operations to SQS queue
    sqs_client = boto3.client("sqs")
    put_money_operations_to_sqs(money_operations, os.environ["money_operations_sqs_queue"], sqs_client)


def put_money_operations_to_sqs(money_operations: Sequence[Dict[str, Any]], sqs_queue_name: str, sqs_client) -> int:
    # gets name of destination SQS queue
    money_operations_queue = sqs_client.get_queue_url(QueueName=sqs_queue_name)

    # generates requests
    msgs = []
    for index, money_operation in enumerate(money_operations):
        msgs.append({
            "Id": str(index),
            "MessageBody": json.dumps(money_operation, default=str)
        })

    # puts it to SQS
    response = sqs_client.send_message_batch(
        QueueUrl=money_operations_queue["QueueUrl"],
        Entries=msgs
    )

    # returns number of added money_operations to queue
    return len(response["Successful"])
