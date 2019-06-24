import os
import json

import money_operation_utils
import money_operations_reports

# import requests
from wallet.aws_utils import read_all_lines_froms3key


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    # loads money operations from csv
    money_op_bucket = os.getenv("money_operations_bucket")
    money_op_file = os.getenv("money_operations_csv_file")
    money_operations_as_csv = read_all_lines_froms3key(money_op_bucket, money_op_file)

    # creates money operations report as dictionary
    money_operations = money_operation_utils.read_money_operations_from_csv(money_operations_as_csv)
    money_oper_report = money_operations_reports.group_by_year_opertype_month_tag(money_operations)

    return {
        "statusCode": 200,
        "body": json.dumps(money_oper_report)
    }
