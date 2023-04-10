import datetime as dt

import pytest

from project.src import form


@pytest.fixture
def formatter():
    return form.OperationFormatter(
        date_format='%d.%m.%Y',
        card_number_format='XXXX XX** **** XXXX',
        number_of_digits_displayed_in_account=4
    )


@pytest.mark.parametrize(
    'account,expected_masked_account',
    [
        ('3523523', '**3523'),
    ]
)
def test_mask_account(formatter, account, expected_masked_account):
    assert formatter.mask_account(account) == expected_masked_account


@pytest.mark.parametrize(
    'card_number,expected_masked_card_number',
    [
        ('1234567890123456', '1234 56** **** 3456'),
    ]
)
def test_mask_card_number(formatter, card_number, expected_masked_card_number):
    assert formatter.mask_card_number(card_number) == expected_masked_card_number


@pytest.mark.parametrize(
    'requisites,expected_form_requisites',
    [
        ('Visa Platinum 1234567890123456', 'Visa Platinum 1234 56** **** 3456'),
        ('Счет 2415251221984719825619', 'Счет **5619'),
    ]
)
def test_format_requisites(formatter, requisites, expected_form_requisites):

    assert formatter.format_requisites(requisites) == expected_form_requisites


@pytest.mark.parametrize(
    'operation,expected_formatted_operation',
    [
        (
            {
                'id': 667307132,
                'state': 'EXECUTED',
                'date': dt.datetime(2019, 7, 13, 18, 51, 29, 313309),
                'operationAmount': {
                    'amount': '97853.86',
                    'currency': {
                        'name': 'руб.',
                        'code': 'RUB'
                    }
                },
                'description': 'Перевод с карты на счет',
                'from': 'Maestro 1308795367077170',
                'to': 'Счет 96527012349577388612'
            },
            """13.07.2019 Перевод с карты на счет
Maestro 1308 79** **** 7170 -> Счет **8612
97853.86 руб."""),
    ]
)
def test_format(formatter, operation, expected_formatted_operation):
    assert formatter.format(operation) == expected_formatted_operation