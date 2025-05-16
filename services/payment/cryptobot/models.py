from pydantic import BaseModel
from enum import StrEnum
from typing import Optional, List, Union
from datetime import datetime


class Assets(StrEnum):
    BTC = "BTC"
    TON = "TON"
    ETH = "ETH"
    USDT = "USDT"
    USDC = "USDC"
    BNB = "BNB"
    TRX = "TRX"
    LTC = "LTC"
    GRAM = "GRAM"
    NOT = "NOT"
    MY = "MY"
    SOL = "SOL"
    DOGS = "DOGS"


class Fiat(StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    BYN = "BYN"
    UAH = "UAH"
    KZT = "KZT"
    UZS = "UZS"
    GEL = "GEL"
    TRY = "TRY"
    AMD = "AMD"
    THB = "THB"
    INR = "INR"
    BRL = "BRL"
    IDR = "IDR"
    AZN = "AZN"
    AED = "AED"
    PLN = "PLN"
    ILS = "ILS"
    KGS = "KGS"
    TJS = "TJS"


class CurrencyType(StrEnum):
    CRYPTO = "crypto"
    FIAT = "fiat"


class Application(BaseModel):
    app_id: int
    name: str
    payment_processing_bot_username: str


class CryptobotError(BaseModel):
    code: int
    name: str


class Balance(BaseModel):
    currency_code: str
    available: Union[float, int]
    onhold: Union[float, int]


class ExchangeRate(BaseModel):
    is_valid: bool
    is_crypto: bool
    is_fiat: bool
    source: str
    target: str
    rate: Union[float, int]


class Invoice(BaseModel):
    invoice_id: int
    status: str
    hash: str
    asset: Optional[str] = None
    amount: Union[int, float]
    bot_invoice_url: str
    web_app_invoice_url: str
    mini_app_invoice_url: str
    description: Optional[str] = None
    created_at: datetime
    allow_comments: bool
    allow_anonymous: bool
    expiration_date: Optional[str] = None
    paid_at: Optional[datetime] = None
    paid_anonymously: Optional[bool] = None
    comment: Optional[str] = None
    hidden_message: Optional[str] = None
    payload: Optional[str] = None
    paid_btn_name: Optional[str] = None
    paid_btn_url: Optional[str] = None
    currency_type: str
    fiat: Optional[str] = None
    paid_asset: Optional[str] = None
    paid_amount: Optional[Union[int, float]] = None
    paid_usd_rate: Optional[Union[int, float]] = None
    paid_fiat_rate: Optional[Union[int, float]] = None
    fee_asset: Optional[str] = None
    fee_amount: Optional[Union[int, float]] = None
    fee_in_usd: Optional[Union[int, float]] = None
    accepted_assets: Optional[Union[List[str], str]] = None
