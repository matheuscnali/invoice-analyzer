from datetime import datetime
from pathlib import Path
from typing import Callable, Literal, Optional

import pandera.pandas as pa
from pandera.typing import DataFrame
from pydantic import BaseModel, FilePath

Banks = Literal['nubank']

InvoiceSource = Literal['nubank', 'mobilis']

class InvoiceTransaction(BaseModel):
    date: datetime
    name: str
    value: float


Invoice = list[InvoiceTransaction]


class CategoryDescription(BaseModel):
    name: str
    max_value: float


class Config(BaseModel):
    invoice_filepath: FilePath
    invoice_source: InvoiceSource
    manual_input_filepath: Optional[FilePath]
    categories: list[CategoryDescription]
    transactions_patterns_by_category: dict[str, list[str]]


class ManualInputDescription(BaseModel):
    remove_from: str
    add_in: str
    value: float
    comment: str

ManualInput = list[ManualInputDescription]


BankInvoiceParse = Callable[[Path], Invoice]


class CategorizedTransactions(pa.DataFrameModel):
    date: datetime
    item: str
    value: float
    category: str


class Analysis(BaseModel):
    categorized_transactions: DataFrame[CategorizedTransactions]
    categories_spent_amount: dict[str, float]
