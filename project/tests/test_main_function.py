import datetime as dt
import pytest

from project.src.main import get_last_executed_operations, convert_date_strings
from project.src.loader import load_operations


@pytest.mark.parametrize(
    'operations,expected_data',
    [
        pytest.param([], [], id='empty list'),
        pytest.param(
            [
                {
                    'id': 441945886,
                    'state': 'EXECUTED',
                    'date': '2019-08-26T10:50:58.294041',
                    'operationAmount': {
                        'amount': '31957.58',
                        'currency': {
                            'name': 'руб.',
                            'code': 'RUB'
                        }
                    },
                    'description': 'Перевод организации',
                    'from': 'Maestro 1596837868705199',
                    'to': 'Счет 64686473678894779589'
                }
            ],
            [
                {
                    'id': 441945886,
                    'state': 'EXECUTED',
                    'date': dt.datetime(2019, 8, 26, 10, 50, 58, 294041),
                    'operationAmount': {
                        'amount': '31957.58',
                        'currency': {
                            'name': 'руб.',
                            'code': 'RUB'
                        }
                    },
                    'description': 'Перевод организации',
                    'from': 'Maestro 1596837868705199',
                    'to': 'Счет 64686473678894779589'
                }
            ],
            id='base case'
        ),
        pytest.param(
            [
                {
                    'id': 441945886,
                    'state': 'EXECUTED',
                    'operationAmount': {
                        'amount': '31957.58',
                        'currency': {
                            'name': 'руб.',
                            'code': 'RUB'
                        }
                    },
                    'description': 'Перевод организации',
                    'from': 'Maestro 1596837868705199',
                    'to': 'Счет 64686473678894779589'
                }
            ],
            [
                {
                    'id': 441945886,
                    'state': 'EXECUTED',
                    'operationAmount': {
                        'amount': '31957.58',
                        'currency': {
                            'name': 'руб.',
                            'code': 'RUB'
                        }
                    },
                    'description': 'Перевод организации',
                    'from': 'Maestro 1596837868705199',
                    'to': 'Счет 64686473678894779589'
                }
            ],
            id='date absent'
        ),
    ]
)
def test_convert_date_strings(operations, expected_data):
    convert_date_strings(operations)
    assert operations == expected_data


@pytest.mark.parametrize(
    'json_filepath,expected_data',
    [
        pytest.param(
            r'operations_without_date.json',
            [],
            id='operations_without_date'
        ),
    ]
)
def test_get_last_executed_operations(load_json_file, json_filepath, expected_data):
    operations = load_json_file(json_filepath)
    last_executed_operations = get_last_executed_operations(operations)
    assert last_executed_operations == expected_data
