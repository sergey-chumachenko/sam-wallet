"""
Unit tests for functions in aws_utils module
"""
import datetime
import json
from unittest.mock import Mock

from aws_utils import read_all_lines_froms3key
from aws_utils import load_money_operations_from_json
import jsondatetime

MONEY_OPERATIONS_JSON = "money_operations.json"

BUCKET_CHUMICK_WALLET = "chumick.wallet"

MONEY_OPERATIONS_CONTENT = """[{
    "date": "2019-05-26",
    "type": "TAKE",
    "sum": 2900,
    "tags": ["children", "school", "Dzi"]
}]"""


def test_read_all_lines_froms3key():
    s3_client = mock_s3_client(MONEY_OPERATIONS_CONTENT)

    actual_result = read_all_lines_froms3key(
        BUCKET_CHUMICK_WALLET,
        MONEY_OPERATIONS_JSON,
        s3_client
    )

    # validates invocations and results
    s3_client.get_object.assert_called_once_with(
        Bucket=BUCKET_CHUMICK_WALLET,
        Key=MONEY_OPERATIONS_JSON
    )
    s3_client.get_object.return_value["Body"].read.called_once()
    s3_client.get_object.return_value["Body"].read.return_value.decode.asser_called_once_with("utf-8")

    assert actual_result == MONEY_OPERATIONS_CONTENT


def test_load_money_operations_from_json():
    dict_money_operations = load_money_operations_from_json(
        BUCKET_CHUMICK_WALLET,
        MONEY_OPERATIONS_JSON,
        mock_s3_client(MONEY_OPERATIONS_CONTENT)
    )

    assert dict_money_operations == [{
        "date": datetime.date(2019, 5, 26),
        "type": "TAKE",
        "sum": 2900,
        "tags": ["children", "school", "Dzi"]
    }]


def test_jsondate_datetime():
    s3_client = mock_s3_client(MONEY_OPERATIONS_CONTENT)

    actual_result = read_all_lines_froms3key(
        BUCKET_CHUMICK_WALLET,
        MONEY_OPERATIONS_JSON,
        s3_client
    )

    money_operations = json.loads(actual_result)

    for money_op in money_operations:
        jsondatetime.iteritems(money_op)


def mock_s3_client(obj_content: str):
    """
    Returns mock object with with interface for reading money operations file in JSON format
    :return: mocked s3 client
    """
    # mocks content of object
    s3_obj_body = Mock()
    s3_obj_body.decode.return_value = obj_content

    # mocks streaming object used to read content of object
    streaming_body = Mock()
    streaming_body.read.return_value = s3_obj_body
    # mocks s3 service to get object with money operations
    s3_client = Mock()
    s3_client.get_object.return_value = {
        "Body": streaming_body
    }
    return s3_client
