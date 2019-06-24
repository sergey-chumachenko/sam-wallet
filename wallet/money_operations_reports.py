from typing import Any
from typing import Dict
from typing import Sequence


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
