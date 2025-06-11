import re
from collections import defaultdict

import pandas as pd
from pandera.typing import DataFrame

from .custom_types import (Analysis, CategorizedTransactions, Config, Invoice,
                           InvoiceTransaction, ManualInput)
from .utils.log import info


def get_category(
    transaction: InvoiceTransaction,
    transactions_patterns_by_category: dict[str, list[str]]
) -> str:
    for c, patterns in transactions_patterns_by_category.items():
        for p in patterns:
            if re.search(p, transaction.name, re.IGNORECASE):
                return c

    return 'unknown'


def analyze(invoice: Invoice, manual_input: ManualInput, config: Config) -> Analysis:
    info('  - Analyzing data')
    c=['date', 'item', 'value', 'category']
    categorized_transactions_df = pd.DataFrame(columns=c)
    categories_spent_amount: dict[str, float] = defaultdict(lambda: float(0))
    for i, t in enumerate(invoice):
        category = get_category(t, config.transactions_patterns_by_category)
        categorized_transactions_df.loc[i]= [
            t.date,
            t.name,
            t.value,
            category
        ]
        categories_spent_amount[category] += t.value

    for m in manual_input:
        categories_spent_amount[m.remove_from] -= m.value
        categories_spent_amount[m.add_in] += m.value

    return Analysis(
        categorized_transactions=DataFrame[CategorizedTransactions](categorized_transactions_df),
        categories_spent_amount=dict(categories_spent_amount)
    )
