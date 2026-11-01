from pathlib import Path

from ..custom_types import BankInvoiceParser, Invoice, InvoiceSource
from ..utils.log import info
from .mobilis import parse_invoice as mobilis_parse_invoice
from .nubank import parse_invoice as nubank_parse_invoice


def get_bank_parse_invoice_fn(invoice_source: InvoiceSource) -> BankInvoiceParser:
    if invoice_source == 'nubank':
        return nubank_parse_invoice
    elif invoice_source == 'mobilis':
        return mobilis_parse_invoice
    raise ValueError(f'Invoice from {invoice_source} is not supported')


def parse_invoice(invoice_filepath: Path, invoice_source: InvoiceSource) -> Invoice:
    info('  - Reading bank invoice')
    bank_parse_invoice_fn = get_bank_parse_invoice_fn(invoice_source)
    return bank_parse_invoice_fn(invoice_filepath)
