import re
from collections import defaultdict

import pandas as pd
from pandera.typing import DataFrame

from .custom_types import (Analysis, CategorizedTransactions, Config, Invoice,
                           InvoiceTransaction, CategoryDescription)
from .utils.log import info


def get_category(
    transaction: InvoiceTransaction,
    categories: list[CategoryDescription]
) -> str:
    for c in categories:
        for p in c.patterns:
            if re.search(p, transaction.name, re.IGNORECASE):
                return c.name

    return 'unknown'


def analyze(invoice: Invoice, config: Config) -> Analysis:
    info('  - Analyzing data')
    c=['date', 'item', 'value', 'category']
    categorized_transactions_df = pd.DataFrame(columns=c)
    categories_spent_amount: dict[str, float] = defaultdict(lambda: float(0))
    for i, t in enumerate(invoice):
        category = get_category(t, config.categories)
        categorized_transactions_df.loc[i]= [
            t.date,
            t.name,
            t.value,
            category
        ]
        categories_spent_amount[category] += t.value

    return Analysis(
        categorized_transactions=DataFrame[CategorizedTransactions](categorized_transactions_df),
        categories_spent_amount=dict(categories_spent_amount)
    )
