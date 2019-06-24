import datetime
from wallet.money_operations_reports import group_by_year_opertype_month_tag


def test_if_list_empty_returns_dict_without_keys():
    money_operations = []
    report = group_by_year_opertype_month_tag(money_operations)
    assert not report


def test_returns_one_item_for_one_money_operation():
    money_operations = [{
        "date": datetime.date(2019, 5, 26),
        "type": "TAKE",
        "sum": 2900.00,
        "tags": ["children", "school", "Dzi"]
    }]

    report = group_by_year_opertype_month_tag(money_operations)

    assert report == {
        2019: {
            "sum": 2900,
            5: {
                "sum": 2900,
                "children": {
                    "sum": 2900,
                    "school": {
                        "sum": 2900,
                        "Dzi": {
                            "sum": 2900
                        }
                    }
                }
            }
        }
    }


def test_two_money_op_with_different_year():
    money_operations = [{
        "date": datetime.date(2019, 5, 26),
        "type": "TAKE",
        "sum": 2900.00,
        "tags": ["children", "school", "Dzi"]
    }, {
        "date": datetime.date(2015, 4, 30),
        "type": "TAKE",
        "sum": 17000,
        "tags": ["rest", "odessa"]
    }]

    report = group_by_year_opertype_month_tag(money_operations)

    assert report == {
        2019: {
            "sum": 2900,
            5: {
                "sum": 2900,
                "children": {
                    "sum": 2900,
                    "school": {
                        "sum": 2900,
                        "Dzi": {
                            "sum": 2900
                        }
                    }
                }
            }
        },
        2015: {
            "sum": 17000,
            4: {
                "sum": 17000,
                "rest": {
                    "sum": 17000,
                    "odessa": {
                        "sum": 17000
                    }
                }
            }
        }
    }


def test_money_op_with_same_year_and_diff_monthes():
    money_operations = [{
        "date": datetime.date(2019, 5, 26),
        "type": "TAKE",
        "sum": 2900.00,
        "tags": ["children", "school", "Dzi"]
    }, {
        "date": datetime.date(2019, 4, 30),
        "type": "TAKE",
        "sum": 17000,
        "tags": ["rest", "odessa"]
    }]

    report = group_by_year_opertype_month_tag(money_operations)

    assert report == {
        2019: {
            "sum": 2900 + 17000,
            5: {
                "sum": 2900,
                "children": {
                    "sum": 2900,
                    "school": {
                        "sum": 2900,
                        "Dzi": {
                            "sum": 2900
                        }
                    }
                }
            },
            4: {
                "sum": 17000,
                "rest": {
                    "sum": 17000,
                    "odessa": {
                        "sum": 17000
                    }
                }
            }
        }
    }


def test_same_year_and_month_nested_tags():
    money_operations = [{
        "date": datetime.date(2019, 5, 26),
        "type": "TAKE",
        "sum": 2900.00,
        "tags": ["children", "school", "Dzi"]
    }, {
        "date": datetime.date(2019, 5, 6),
        "type": "TAKE",
        "sum": 210,
        "tags": ["children", "dances", "dzi"]
    }, {
        "date": datetime.date(2019, 5, 6),
        "type": "TAKE",
        "sum": 210,
        "tags": ["children", "dances", "zlata"]
    }, {
        "date": datetime.date(2019, 5, 6),
        "type": "TAKE",
        "sum": 225,
        "tags": ["food"]
    }]

    report = group_by_year_opertype_month_tag(money_operations)

    assert report == {
        2019: {
            "sum": 2900 + 210 + 210 + 225,
            5: {
                "sum": 2900 + 210 + 210 + 225,
                "children": {
                    "sum": 2900 + 210 + 210,
                    "school": {
                        "sum": 2900,
                        "Dzi": {
                            "sum": 2900
                        }
                    },
                    "dances": {
                        "sum": 210 + 210,
                        "dzi": {
                            "sum": 210
                        },
                        "zlata": {
                            "sum": 210
                        }
                    }
                },
                "food": {
                    "sum": 225
                }
            }
        }
    }
