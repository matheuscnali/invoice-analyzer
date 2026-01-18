from pathlib import Path
from typing import Optional

from ..custom_types import (BankInvoiceParse, Invoice, ManualInput,
                            ManualInputDescription, InvoiceSource)
from ..utils.fs import read_yaml
from ..utils.log import info
from .nubank import parse_invoice as nubank_parse_invoice
from .mobilis import parse_invoice as mobilis_parse_invoice


def get_bank_parse_invoice_fn(invoice_source: InvoiceSource) -> BankInvoiceParse:
    if invoice_source == 'nubank':
        return nubank_parse_invoice
    elif invoice_source == 'mobilis':
        return mobilis_parse_invoice
    raise ValueError(f'Invoice from {invoice_source} is not supported')


def parse_manual_input(filepath: Optional[Path]) -> ManualInput:
    if filepath is None:
        return []

    info('  - Reading manual input')
    return ManualInput([ManualInputDescription(**m) for m in read_yaml(filepath)])


def parse_invoice(invoice_filepath: Path, invoice_source: InvoiceSource) -> Invoice:
    info('  - Reading bank invoice')
    bank_parse_invoice_fn = get_bank_parse_invoice_fn(invoice_source)
    return bank_parse_invoice_fn(invoice_filepath)
