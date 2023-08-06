from __future__ import annotations
from requests import get
from json import loads
import asyncio
import aiohttp


from functools import wraps
 
from asyncio.proactor_events import _ProactorBasePipeTransport
 

"""Это фиск RuntimeError. (Не выводит громоздкий варнинг на всю консоль.)"""
def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper
 
_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)


class Payment():
    """Класс сгенерированной оплаты.
    """

    def __init__(self, payment_id : str, default_params : dict, amount : int = None) -> Payment:
        self.id = payment_id
        self.default_params = default_params
        self.url = f"https://pay.crystalpay.ru/?i={self.id}"
        self.api_url = "https://api.crystalpay.ru/v1/"
        self.paymethod = None

    async def if_paid(self) -> bool:
        params = self.default_params
        params['o'] = "invoice-check"
        params['i'] = self.id

        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url, params=params) as resp:
                data = loads(await resp.text())


        if data['auth'] != 'ok':
            raise AuthError("Не смог проверить оплату платежа! Ошибка авторизации!")
        if data['error']:
            raise CheckPaymentErr(f"Ошибка проверки платежа: {data['error_message']}")

        if data['state'] == "payed":
            self.paymethod = data['paymethod']
            return True
        else:
            return False
    
    async def get_amount(self) -> None:
        params = self.default_params
        params['o'] = "invoice-check"
        params['i'] = self.id
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url, params=params) as resp:
                data = loads(await resp.text())

        if data['auth'] != 'ok':
            raise AuthError("Не смог проверить оплату платежа! Ошибка авторизации!")
        if data['error']:
            raise CheckPaymentErr(f"Ошибка проверки платежа: {data['error_message']}")
        self.amount = data['amount']

class CrystalPay(object):


    def __init__(self, cash_name : str, secret_1 : str) -> CrystalPay:
        """cash_name - имя кассы/логин
        secret_1 - секретный ключ 1
        """
        self.cash_name = cash_name
        self.secret_1 = secret_1
        self.api_url = "https://api.crystalpay.ru/v1/"
        self.def_params = dict(s=self.secret_1, n=self.cash_name, o = None)

        

    async def get_cash_balance(self) -> list:
        """Получение баланса кассы.
        """
        temp_params = self.def_params
        temp_params['o'] = "balance" 
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url, params=temp_params) as resp:
                data = loads(await resp.text())

        if data['auth'] != "ok":
            raise AuthError("Не удалось получить баланс кассы! Ошибка авторизации!")
        return data['balance']

    async def create_invoice(self,
        amount : int,
        currency : str = None,
        lifetime : int = None,
        redirect : str = None,
        callback : str = None,
        extra : str = None,
        payment_system : str = None,
        ) -> Payment:
        """Метод генерации ссылки для оплаты 
        amount - сумма на оплату(целочисл.)
        currency - 	Валюта суммы (конвертируется в рубли) (USD, BTC, ETH, LTC…) (необязательно)
        liftetime - Время жизни счёта для оплаты, в минутах (необязательно)
        redirect - Ссылка для перенаправления после оплаты (необязательно)
        callback - Ссылка на скрипт, на который будет отправлен запрос, после успешного зачисления средств на счёт кассы (необязательно)
        extra - Любые текстовые данные, пометка/комментарий. Будет передано в callback или при проверке статуса платежа (необязательно)
        payment_system - Если нужно принудительно указать платежную систему (необязательно).
        """

        temp_params = self.def_params
        temp_params['o'] = "invoice-create"
        temp_params['amount'] = amount

        if currency:
            temp_params['currency'] = currency
        if lifetime:
            temp_params['liftetime'] = lifetime
        if redirect:
            temp_params['redirect'] = redirect
        if callback:
            temp_params['callback'] = callback
        if extra:
            temp_params['extra'] = extra
        if payment_system:
            temp_params['m'] = payment_system

        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url, params=temp_params) as resp:
                data = loads(await resp.text())
        if data['auth'] != 'ok':
            raise AuthError("Не смог создать платеж! Ошибка авторизации!")
        if data['error']:
            raise CreatePaymentError(f"Ошибка создания платежа: {data['error_message']}")

        return Payment(data['id'], self.def_params, amount)


    async def construct_payment_by_id(self, paymnet_id) -> Payment:
        payment = Payment(paymnet_id, self.def_params)
        await payment.get_amount()
        return payment
        


class AuthError(Exception):
    pass

class CreatePaymentError(Exception):
    pass

class CheckPaymentErr(Exception):
    pass
