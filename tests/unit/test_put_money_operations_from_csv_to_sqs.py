from datetime import date
from unittest.mock import Mock

from hello_world.put_money_operations_from_csv_to_sqs import get_file_name_with_money_operations
from hello_world.put_money_operations_from_csv_to_sqs import put_money_operations_to_sqs
from hello_world.put_money_operations_from_csv_to_sqs import lambda_handler


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
            "Id": 0,
            "MessageBody": money_operation_a
        }
        sqs_client = self.mock_boto3_sqs_client(money_operation_a, sqs_entry)

        sqs_queue_name = "MoneyOperationsQueue"
        num_successful = put_money_operations_to_sqs(money_operations, sqs_queue_name, sqs_client)

        sqs_client.get_queue_url.assert_called_once_with(QueueName=sqs_queue_name)
        sqs_client.send_message_batch.assert_called_once_with(
            QueueUrl=sqs_client.get_queue_url.return_value.QueueUrl,
            Entries=[sqs_entry]
        )
        assert num_successful == len(money_operations)

    # def test_lambda_handler(self):
    #     event = {
    #         "Records": [{
    #             "s3": {
    #                 "bucket": {
    #                     "name": "wallet_1024"
    #                 },
    #                 "object": {
    #                     "key": "money_operations.csv"
    #                 }
    #             }
    #         }]
    #     }
    #
    #     # mocks aws_utils
    #     all_money_operations_as_csv = "2019-06-23,TAKE,500,car parking"
    #     aws_utils = Mock()
    #     aws_utils.read_all_lines_froms3key.return_value = all_money_operations_as_csv
    #
    #     # mocks money_operation_utils
    #     money_operation_a = {
    #         "date": date(2019, 6, 23),
    #         "type": "TAKE",
    #         "sum": 500,
    #         "tags": ["car", "parking"]
    #     }
    #     money_operations = [money_operation_a]
    #     money_operation_utils = Mock()
    #     money_operation_utils.read_money_operations_from_csv.return_value = money_operations
    #
    #     # mocks boto3
    #     sqs_entry = {
    #         "Id": 0,
    #         "MessageBody": money_operation_a
    #     }
    #     boto3 = Mock()
    #     boto3.client.return_value = self.mock_boto3_sqs_client(money_operation_a, sqs_entry)
    #
    #     # mocks os
    #     os = Mock()
    #     os.environ.return_value = {
    #         "money_operations_sqs_queue": "MoneyOperationsQueue"
    #     }
    #
    #     lambda_handler(event, None)
    #
    #     aws_utils.read_all_lines_froms3key.assert_called_once_with("wallet_1024", "money_operations.csv")
    #     money_operation_utils.read_money_operations_from_csv.assert_called_once_with(all_money_operations_as_csv)
    #     boto3.client.assert_called_once_with("sqs")

    def mock_boto3_sqs_client(self, money_operation_a, sqs_entry):
        queue_url_responce = Mock()
        queue_url_responce.QueueUrl.return_value = "money_operations_queue"
        sqs_client = Mock()
        sqs_client.get_queue_url.return_value = queue_url_responce
        sqs_client.send_message_batch.return_value = {
            "Successful": [sqs_entry]
        }
        return sqs_client
