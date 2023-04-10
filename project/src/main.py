import datetime as dt

from project.src import loader
from project.src.form import OperationFormatter

INITIAL_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
EXECUTED_OPERATION_STATE = 'EXECUTED'

DISPLAYED_OPERATION_COUNT = 5

RESULT_DATE_FORMAT = '%d.%m.%Y'
CARD_NUMBER_FORMAT = 'XXXX XX** **** XXXX'
NUMBER_OF_DIGITS_DISPLAYED_IN_ACCOUNT = 4

"""
convert_date_strings: функция, конвертурующая, далее при применении метода get() возвращаем значение для указанного ключа,
если возвращаемое значение не None, то timestamp возвращает объект datetime соответствующий date_string проанализированный
в соответствии с указанным форматом INITIAL_DATE_FORMAT.
:param operations: переменная, которая используя ключ date, предотавляет соответствующее значение
    
"""


def convert_date_strings(operations):
    for operation in operations:
        date_string = operation.get('date')

        if date_string is not None:
            timestamp = dt.datetime.strptime(date_string, INITIAL_DATE_FORMAT)
            operation['date'] = timestamp


"""
get_last_executed_operations: функция, фильтрующая, далее при применении функции lambda произведена сортировка списка
по ключу, а также устанавливается сколько выполненных операций DISPLAYED_OPERATION_COUNT.
"""


def get_last_executed_operations(operations):
    operations_with_date = filter(
        lambda operation: (
                'date' in operation and operation['state'] == EXECUTED_OPERATION_STATE
        ),
        operations
    )
    return sorted(
        operations_with_date,
        key=lambda operation: operation['date'],
        reverse=True,
    )[:DISPLAYED_OPERATION_COUNT]


def main():
    operations = loader.load_operations()

    convert_date_strings(operations)
    last_executed_operations = get_last_executed_operations(operations)
    formatter = OperationFormatter(
        date_format=RESULT_DATE_FORMAT,
        card_number_format=CARD_NUMBER_FORMAT,
        number_of_digits_displayed_in_account=(
            NUMBER_OF_DIGITS_DISPLAYED_IN_ACCOUNT
        ),
    )

    formatted_operations = []
    for operation in last_executed_operations:
        formatted_operations.append(formatter.format(operation))

    print('\n\n'.join(formatted_operations))


if __name__ == '__main__':
    main()
