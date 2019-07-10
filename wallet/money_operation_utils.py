import csv
import io
import json
from datetime import datetime
from typing import Sequence, Dict, Any


PROPERTY_TAGS = 'tags'
PROPERTY_SUM = 'sum'
PROPERTY_TYPE = 'type'
PROPERTY_DATE = 'date'


def read_money_operations_from_csv(money_op_as_csv: str) -> Sequence[Dict[str, Any]]:
    """
    Each row contains the four comma separated money operation's properties: date, type, sum, tags.

    The 'date' field is a string formatted as ISO_DATE(YYYY-MM-DD)
    The 'type' can be PUT or TAKE
    The 'sum' value is a float
    The 'tags' space separated words
    It will be parsed and assigned to according key in dictionary.

    :param money_op_as_csv: text as a list of rows in CSV-format
    :return: list of dictionaries. Each element represents row in money_op_as_csv
    """

    str_io = io.StringIO(money_op_as_csv.strip())
    reader = csv.DictReader(str_io, [PROPERTY_DATE, PROPERTY_TYPE, PROPERTY_SUM, PROPERTY_TAGS])
    money_operations = []
    for row in reader:
        op_date = datetime.strptime(row[PROPERTY_DATE].strip(), '%Y-%m-%d').date()
        op_type = row[PROPERTY_TYPE].strip()
        op_sum = float(row[PROPERTY_SUM].strip())
        op_tags = row[PROPERTY_TAGS].strip().split(" ")

        money_operations.append({
            PROPERTY_DATE: op_date,
            PROPERTY_TYPE: op_type,
            PROPERTY_SUM: op_sum,
            PROPERTY_TAGS: op_tags
        })
    return money_operations


def save_to_s3(money_operations: Sequence[Dict[str, Any]], dest_s3_bucket: str, dest_s3_obj_key: str, s3_client) -> None:
    s3_client.put_object(
        Bucket=dest_s3_bucket,
        Key=dest_s3_obj_key,
        Body=json.dumps(money_operations, default=str)
    )
