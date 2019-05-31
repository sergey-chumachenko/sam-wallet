import datetime
from hello_world.money_operations_reports import create_money_operations_from_csv


def test_returns_empty_list_if_empty_text():
    assert create_money_operations_from_csv("") == []


def test_returns_list_with_size_equals_to_num_rows():
    csv = """\
    2019-05-29,TAKE,127.54,food fruits
    2019-03-08,TAKE,200,cinema
    2019-02-02,TAKE,2000,children school
    2019-04-26,PUT,112728,deposit
    2019-03-11,TAKE,2312.54,children first two
    """
    money_operations = create_money_operations_from_csv(csv)

    assert len(money_operations) == 5

    assert money_operations == [{
        "date": datetime.date(2019, 5, 29),
        "type": "TAKE",
        "sum": 127.54,
        "tags": ["food", "fruits"]
    }, {
        "date": datetime.date(2019, 3, 8),
        "type": "TAKE",
        "sum": 200,
        "tags": ["cinema"]
    }, {
        "date": datetime.date(2019, 2, 2),
        "type": "TAKE",
        "sum": 2000,
        "tags": ["children", "school"]
    }, {
        "date": datetime.date(2019, 4, 26),
        "type": "PUT",
        "sum": 112728,
        "tags": ["deposit"]
    }, {
        "date": datetime.date(2019, 3, 11),
        "type": "TAKE",
        "sum": 2312.54,
        "tags": ["children", "first", "two"]
    }]
