import datetime

from wallet.money_operations_reports import group_by_year_month_tag


def test_if_list_empty_returns_dict_without_keys():
    money_operations = []
    report = group_by_year_month_tag(money_operations)
    assert not report


def test_returns_one_item_for_one_money_operation():
    money_operations = [{
        "date": datetime.date(2019, 5, 26),
        "type": "TAKE",
        "sum": 2900,
        "tags": ["children", "school", "Dzi"]
    }]

    report = group_by_year_month_tag(money_operations)

    assert report == [{
        "group_name": "2019",
        "total_sum": 2900,
        "sub_groups": [{
            "group_name": "5",
            "total_sum": 2900,
            "sub_groups": [{
                "group_name": "children",
                "total_sum": 2900,
                "sub_groups": [{
                    "group_name": "school",
                    "total_sum": 2900,
                    "sub_groups": [{
                        "group_name": "Dzi",
                        "total_sum": 2900,
                        "sub_groups": []
                    }]
                }]
            }]
        }]
    }]


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

    report = group_by_year_month_tag(money_operations)

    assert report == [
        {
            "group_name": "2019",
            "total_sum": 2900,
            "sub_groups": [{
                "group_name": "5",
                "total_sum": 2900,
                "sub_groups": [{
                    "group_name": "children",
                    "total_sum": 2900,
                    "sub_groups": [{
                        "group_name": "school",
                        "total_sum": 2900,
                        "sub_groups": [{
                            "group_name": "Dzi",
                            "total_sum": 2900,
                            "sub_groups": []
                        }]
                    }]
                }]
            }]
        },
        {
            "group_name": "2015",
            "total_sum": 17000,
            "sub_groups": [{
                "group_name": "4",
                "total_sum": 17000,
                "sub_groups": [{
                    "group_name": "rest",
                    "total_sum": 17000,
                    "sub_groups": [{
                        "group_name": "odessa",
                        "total_sum": 17000,
                        "sub_groups": []
                    }]
                }]
            }]
        }
    ]


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

    report = group_by_year_month_tag(money_operations)

    assert report == [
        {
            "group_name": "2019",
            "total_sum": 19900,
            "sub_groups": [
                {
                    "group_name": "5",
                    "total_sum": 2900,
                    "sub_groups": [{
                        "group_name": "children",
                        "total_sum": 2900,
                        "sub_groups": [{
                            "group_name": "school",
                            "total_sum": 2900,
                            "sub_groups": [{
                                "group_name": "Dzi",
                                "total_sum": 2900,
                                "sub_groups": []
                            }]
                        }]
                    }]
                },
                {
                    "group_name": "4",
                    "total_sum": 17000,
                    "sub_groups": [{
                        "group_name": "rest",
                        "total_sum": 17000,
                        "sub_groups": [{
                            "group_name": "odessa",
                            "total_sum": 17000,
                            "sub_groups": []
                        }]
                    }]
                }
            ]
        }
    ]


def test_same_year_and_month_nested_tags():
    money_operations = [{
        "date": datetime.date(2019, 5, 26),
        "type": "TAKE",
        "sum": 2900,
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

    report = group_by_year_month_tag(money_operations)

    assert report == [{
        "group_name": "2019",
        "total_sum": 2900 + 210 + 210 + 225,
        "sub_groups": [{
            "group_name": "5",
            "total_sum": 2900 + 210 + 210 + 225,
            "sub_groups": [
                {
                    "group_name": "children",
                    "total_sum": 2900 + 210 + 210,
                    "sub_groups": [
                        {
                            "group_name": "school",
                            "total_sum": 2900,
                            "sub_groups": [{
                                "group_name": "Dzi",
                                "total_sum": 2900,
                                "sub_groups": []
                            }]
                        },
                        {
                            "group_name": "dances",
                            "total_sum": 210 + 210,
                            "sub_groups": [
                                {
                                    "group_name": "dzi",
                                    "total_sum": 210,
                                    "sub_groups": []
                                },
                                {
                                    "group_name": "zlata",
                                    "total_sum": 210,
                                    "sub_groups": []
                                }
                            ]
                        }
                    ]
                },
                {
                    "group_name": "food",
                    "total_sum": 225,
                    "sub_groups": []
                }
            ]
        }]
    }]
