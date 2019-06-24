import json
from datetime import date
from unittest.mock import Mock

from wallet.put_money_operations_from_csv_to_sqs import get_file_name_with_money_operations
from wallet.put_money_operations_from_csv_to_sqs import put_money_operations_to_sqs


class TestPutMoneyOperationsFromCsvToSqs():
    def test_get_file_name_with_money_operations(self):
        event = {
            "Records": [{
                "s3": {
                    "bucket": {
                        "name": "wallet_1024"
                    },
                    "object": {
                        "key": "money_operations.csv"
                    }
                }
            }]
        }

        assert get_file_name_with_money_operations(event) == {
            "bucket": "wallet_1024",
            "key": "money_operations.csv"
        }

    def test_put_money_operations_to_sqs(self):
        money_operation_a = {
            "date": date(2019, 6, 23),
            "type": "TAKE",
            "sum": 500,
            "tags": ["car", "parking"]
        }
        money_operations = [money_operation_a]

        # mocks boto3 SQS client
        sqs_entry = {
            "Id": str(0),
            "MessageBody": json.dumps(money_operation_a, default=str)
        }
        sqs_client = self.mock_boto3_sqs_client(sqs_entry)

        sqs_queue_name = "MoneyOperationsQueue"
        num_successful = put_money_operations_to_sqs(money_operations, sqs_queue_name, sqs_client)

        sqs_client.get_queue_url.assert_called_once_with(QueueName=sqs_queue_name)
        sqs_client.send_message_batch.assert_called_once_with(
            QueueUrl=sqs_client.get_queue_url.return_value["QueueUrl"],
            Entries=[sqs_entry]
        )
        assert num_successful == len(money_operations)

    def mock_boto3_sqs_client(self, sqs_entry):
        sqs_client = Mock()
        sqs_client.get_queue_url.return_value = {
            "QueueUrl": "money_operations_queue"
        }
        sqs_client.send_message_batch.return_value = {
            "Successful": [sqs_entry]
        }
        return sqs_client
