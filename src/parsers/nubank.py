from datetime import datetime

import pandas as pd

from ..custom_types import Invoice, InvoiceTransaction


def parse_invoice(invoice_filepath) -> Invoice:
    columns_names = ['date', 'title', 'amount']
    transactions = []
    for _, e in pd.read_csv(invoice_filepath, skiprows=1, names=columns_names).iterrows():
        transactions.append(InvoiceTransaction(
            date=datetime.strptime(e['date'], '%Y-%m-%d'),
            name=e['title'],
            value=float(e['amount'])
        ))
    return transactions
