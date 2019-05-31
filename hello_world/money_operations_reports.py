import csv
import io
from typing import Any
from typing import Dict
from typing import Sequence

from datetime import datetime


def create_money_operations_from_csv(money_op_as_csv: str) -> Sequence[Dict[str, Any]]:
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
    PROPERTY_TAGS = 'tags'
    PROPERTY_SUM = 'sum'
    PROPERTY_TYPE = 'type'
    PROPERTY_DATE = 'date'

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


def group_by_year_opertype_month_tag(money_operations: Sequence[Dict[str, Any]]) -> Dict[str, Dict]:
    report = {}
    for money_operation in money_operations:
        year_details = report.setdefault(money_operation["date"].year, {"sum": 0.0})
        year_details["sum"] += money_operation["sum"]

        month_details = year_details.setdefault(money_operation["date"].month, {"sum": 0.0})
        month_details["sum"] += money_operation["sum"]

        if money_operation["tags"]:
            tags = money_operation["tags"]
            tag_details = month_details.setdefault(tags[0], {"sum": 0.0})
            tag_details["sum"] += money_operation["sum"]

            tag_index = 1
            while tag_index < len(tags):
                tag_details = tag_details.setdefault(tags[tag_index], {"sum": 0.0})
                tag_details["sum"] += money_operation["sum"]
                tag_index += tag_index

    return report
