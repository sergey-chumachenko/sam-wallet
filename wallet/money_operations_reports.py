from typing import Any
from typing import Dict
from typing import Optional
from typing import Sequence


def find_report_group(report_groups: Sequence[Dict], group_name: str) -> Optional[Dict]:
    for report_group in report_groups:
        if report_group.get("group_name") == group_name:
            return report_group
    return None


def append_report_group(report_groups: Sequence[Dict], group_name: str) -> Dict[str, Any]:
    report_group = find_report_group(report_groups, group_name)
    if not report_group:
        report_groups.append({
            "group_name": group_name,
            "total_sum": 0,
            "sub_groups": []
        })
    return report_groups[-1]


def group_by_year_month_tag(money_operations: Sequence[Dict[str, Any]]) -> Sequence[Dict]:
    report = []
    for money_operation in money_operations:
        year_details = append_report_group(report, str(money_operation["date"].year))
        year_details["total_sum"] += money_operation["sum"]

        month_details = append_report_group(year_details["sub_groups"], str(money_operation["date"].month))
        month_details["total_sum"] += money_operation["sum"]

        if money_operation["tags"]:
            tags = money_operation["tags"]
            tag_details = append_report_group(month_details["sub_groups"], tags[0])
            tag_details["total_sum"] += money_operation["sum"]

            tag_index = 1
            while tag_index < len(tags):
                tag_details = append_report_group(tag_details["sub_groups"], tags[tag_index])
                tag_details["total_sum"] += money_operation["sum"]
                tag_index += tag_index

    return report
