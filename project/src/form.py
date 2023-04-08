class OperationFormatter:
    def __init__(
        self,
        date_format=None,
        card_number_format=None,
        number_of_digits_displayed_in_account=None
    ):
        self.date_format = date_format
        self.card_number_format = card_number_format
        self.number_of_digits_displayed_in_account = (
            number_of_digits_displayed_in_account
        )

    def format(self, operation):
        formatted_date = operation['date'].strftime(self.date_format)
        description = operation['description']

        raw_from = operation.get('from')
        from_ = self.format_requisites(raw_from) if raw_from is not None else ''

        raw_to = operation.get('to')
        to_ = self.format_requisites(raw_to) if raw_to is not None else ''

        amount = operation['operationAmount']['amount']
        currency_name = operation['operationAmount']['currency']['name']

        return f"""{formatted_date} {description}
{from_} -> {to_}
{amount} {currency_name}"""

    def mask_card_number(self, card_number):
        if len(card_number) != len(self.card_number_format.replace(' ', '')):
            raise Exception(
                f'Card number {card_number} cannot be'
                f'masked with a mask {self.card_number_format}'
            )
        i = 0
        symbols = []
        for mask_symbol in self.card_number_format:
            if mask_symbol == 'X':
                symbols.append(card_number[i])
                i += 1
            elif mask_symbol == '*':
                symbols.append('*')
                i += 1
            else:
                symbols.append(mask_symbol)

        return ''.join(symbols)

    def mask_account(self, account):
        if len(account) < self.number_of_digits_displayed_in_account + 2:
            raise Exception(
                f' Incorrect account number: {account}. '
                'The number of digits must be greater that'
                f'{self.number_of_digits_displayed_in_account + 2}'
            )
        return '**' + account[-self.number_of_digits_displayed_in_account:]

    def format_requisites(self, requisites_string):
        title, digits = requisites_string.rsplit(maxsplit=1)
        if title.startswith('Счет') or title.startswith('Счёт'):
            masked_account = self.mask_account(digits)
            return f'{title} {masked_account}'
        else:
            masked_card_number = self.mask_card_number(digits)
            return f'{title} {masked_card_number}'