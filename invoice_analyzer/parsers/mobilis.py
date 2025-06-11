from datetime import datetime

import pandas as pd

from ..custom_types import Invoice, InvoiceTransaction


def parse_invoice(invoice_filepath) -> Invoice:
    columns_names = ['date', 'title', 'category', 'amount']
    transactions = []
    for _, e in pd.read_csv(invoice_filepath, skiprows=1, sep=';', names=columns_names).iterrows():
        transactions.append(InvoiceTransaction(
            date=datetime.strptime(e['date'], '%d/%m/%Y'),
            name=e['title'],
            value=float(e['amount'].strip('R$').replace(',', '.'))
        ))
    return transactions
