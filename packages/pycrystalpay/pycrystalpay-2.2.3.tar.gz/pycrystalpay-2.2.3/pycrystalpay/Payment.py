from __future__ import annotations
from re import L
from requests import get
from json import loads


class Payment():
    """Класс сгенерированной оплаты.
    """

    def __init__(self, payment_id : str, default_params) -> Payment:
        self.id = payment_id
        self.default_params = default_params
        self.url = f"https://pay.crystalpay.ru/?i={self.id}"
        self.api_url = "https://api.crystalpay.ru/v1/"
        self.paymethod = None
        self.amount = None

    def if_payed(self) -> bool:
        params = self.default_params
        params['o'] = "invoice-check"
        params['i'] = self.id

        data = loads(get(self.api_url, params=params).text)

        if data['state'] in ["notpayed", "processing"]:
            return False
        else:
            self.paymethod = data['paymethod']
            self.amount = data['amount']
            return True
        
