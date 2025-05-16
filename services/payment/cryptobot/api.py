from tg_bot.infra.request_client import RequestClient, Method
from tg_bot.services.payment.cryptobot.models import *
from tg_bot.services.payment.cryptobot.config import cryptobot_api_settings

from typing import Union


class CryptobotApi(RequestClient):
    """
    Инициализация API клиента для платежного
    сервиса cryptobot.t.me

    DOCS: https://help.crypt.bot/crypto-pay-api
    """

    def __init__(
            self,
            api_key: str,
            testnet: bool = False
    ):
        """
        Инициализация переменных платежного API
        :param api_key: str
        """
        super().__init__()
        self._API_KEY = api_key
        self._HEADERS_ = {
            "Crypto-Pay-API-Token": self._API_KEY
        }
        if testnet:
            self.API_HOST = "https://testnet-pay.crypt.bot/"
        else:
            self.API_HOST = "https://pay.crypt.bot/api"

    async def get_me(self) -> Union[Application, CryptobotError]:
        """
        Получаем информацию о приложении API
        :return: Application or CryptobotError
        """
        url = f"{self.API_HOST}/getMe"

        response = await self.request(
            method=Method.GET,
            url=url,
            headers=self._HEADERS_
        )
        dictionary = await response.json()
        if response.status == 200:
            return Application(**dictionary["result"])
        return CryptobotError(**dictionary["error"])

    async def get_balance(
            self,
    ) -> Union[List[Balance], CryptobotError]:
        url = f"{self.API_HOST}/getBalance"

        response = await self.request(
            method=Method.GET,
            url=url,
            headers=self._HEADERS_
        )
        dictionary = await response.json()

        if response.status == 200:
            data = dictionary["result"]
            return [Balance(**i) for i in data]
        return CryptobotError(**dictionary["error"])

    async def get_exchange_rates(
            self
    ) -> Union[List[ExchangeRate], CryptobotError]:
        """
        Получаем курс валют в Cryptobot
        :return: List ExchangeRates obj or CryptobotError obj
        """
        url = f"{self.API_HOST}/getExchangeRates"
        response = await self.request(
            method=Method.GET,
            url=url,
            headers=self._HEADERS_
        )
        dictionary = await response.json()

        if response.status == 200:
            data = dictionary["result"]
            return [ExchangeRate(**i) for i in data]

        return CryptobotError(**dictionary["error"])

    async def create_invoice(
            self,
            amount: Union[float, int],
            asset: Optional[Union[Assets, str]] = None,
            description: Optional[str] = None,
            hidden_message: Optional[str] = None,
            paid_btn_name: Optional[str] = None,
            paid_btn_url: Optional[str] = None,
            payload: Optional[str] = None,
            allow_comments: Optional[bool] = None,
            allow_anonymous: Optional[bool] = None,
            expires_in: Optional[int] = None,
            fiat: Optional[str] = None,
            currency_type: Optional[CurrencyType | str] = None,
            accepted_assets: Optional[Union[List[Assets | str], str]] = None,
    ) -> Union[Invoice, CryptobotError]:
        """
        Создание счета на оплату с заданными параметрами
        :param amount: float or int (сумма оплаты)
        :param asset: Asset obj or str (крипта для оплаты)
        :param description: str (описание счета)
        :param hidden_message: str (текст сообщения, которое будет показано пользователю после оплаты счета. Не более 248 символов.)
        :param paid_btn_name: str (Название кнопки, которая будет показана пользователю после оплаты счета.)
        :param paid_btn_url: str (Требуется, если используется paid_btn_name. Вы можете указать любую ссылку на успех (например, ссылку на вашего бота). Начинается с https или http.)
        :param payload: str (любые данные, которые вы хотите добавить к счету (например, идентификатор пользователя, идентификатор платежа и т.д.). Размер до 4 Кб.)
        :param allow_comments: bool (разрешать пользователю оставлять комментарий к счету)
        :param allow_anonymous: bool (разрешать пользователю анонимный платеж)
        :param expires_in: int (Вы можете установить срок оплаты счета в секундах. Принимаются значения от 1 до 2678400.)
        :param fiat: str (Код валюты, если в поле currency_type указано значение fiat. Поддерживаемые валюты: все фиатные валюты в CryptoBot.)
        :param currency_type: CurrencyType obj or str (Тип цены, может быть “crypto” или “fiat”. По умолчанию используется crypto.)
        :param accepted_assets: list Assets or str OR str (Активы, которые могут быть использованы для оплаты счета, если поле fiat имеет значение. Поддерживаемые активы: “USDT”, “TON”, “BTC” )
        :return: Invoice obj or CryptobotError obj
        """
        url = f"{self.API_HOST}/createInvoice"
        if accepted_assets and isinstance(accepted_assets, list):
            accepted_assets = ",".join(map(str, accepted_assets))

        params = {
            "asset": asset,
            "amount": amount,
            "description": description,
            "hidden_message": hidden_message,
            "paid_btn_name": paid_btn_name,
            "paid_btn_url": paid_btn_url,
            "payload": payload,
            "allow_comments": allow_comments,
            "allow_anonymous": allow_anonymous,
            "expires_in": expires_in,
            "fiat": fiat,
            "currency_type": currency_type,
            "accepted_assets": accepted_assets,
        }

        for key, value in params.copy().items():
            if isinstance(value, bool):
                params[key] = str(value).lower()
            if value is None:
                del params[key]

        response = await self.request(
            method=Method.GET,
            url=url,
            params=params,
            headers=self._HEADERS_
        )
        dictionary = await response.json()

        if response.status == 200:
            return Invoice(**dictionary["result"])

        return CryptobotError(**dictionary["error"])

    async def get_invoices(
            self,
            asset: Optional[Union[Assets, str]] = None,
            invoice_ids: Optional[Union[List[int], int]] = None,
            status: Optional[str] = None,
            offset: Optional[int] = None,
            count: Optional[int] = None,
    ):
        """
        Получаем инвойс\инвойсы с API
        :param asset: Asset or str (необязательный параметр, монета инвойсов)
        :param invoice_ids: list int or int (необязательный, но с ним работать будем, id инвойсов\инвойса)
        :param status: str (статус инвойсов), необязательный
        :param offset: int
        :param count: int
        :return:
        """
        url = f"{self.API_HOST}/getInvoices"
        if invoice_ids and isinstance(invoice_ids, list):
            invoice_ids = ",".join(map(str, invoice_ids))

        params = {
            "asset": asset,
            "invoice_ids": invoice_ids,
            "status": status,
            "offset": offset,
            "count": count,
        }

        for key, value in params.copy().items():
            if value is None:
                del params[key]

        response = await self.request(
            method=Method.GET,
            url=url,
            params=params,
            headers=self._HEADERS_
        )
        dictionary = await response.json()

        if response.status == 200:
            if invoice_ids and isinstance(invoice_ids, int):
                return Invoice(**dictionary["result"]["items"][0])

            return [Invoice(**invoice) for invoice in dictionary["result"]["items"]]

        return CryptobotError(**dictionary["error"])

    async def is_success(
            self,
            invoice_id: Optional[int],
    ) -> bool:
        """
        Функция проверки оплачен ли инвойс для оплаты
        :param invoice_id: int or str
        :return: bool
        """
        invoice = await self.get_invoices(
            invoice_ids=invoice_id
        )
        if isinstance(invoice, Invoice):
            return invoice.status == "paid"

        return False


cryptobot_api = CryptobotApi(
    api_key=cryptobot_api_settings.CRYPTOBOT_API_TOKEN,
    testnet=False
)
