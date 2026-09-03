from datetime import datetime
from pathlib import Path
from typing import Callable, Literal

import pandera.pandas as pa
import pandas as pd
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
    patterns: list[str]

class Config(BaseModel):
    invoice_filepath: FilePath
    invoice_source: InvoiceSource
    categories: list[CategoryDescription]

BankInvoiceParser = Callable[[Path], Invoice]

class CategorizedTransactions(pa.DataFrameModel):
    date: datetime
    item: str
    value: float
    category: str


class Analysis(BaseModel):
    categorized_transactions: pd.DataFrame
    categories_spent_amount: dict[str, float]

    class Config:
        arbitrary_types_allowed = True
