from datetime import datetime
from typing import Optional, Tuple, cast

import pandas as pd

from .custom_types import Analysis, CategoryDescription, Config
from .utils.log import info


def get_category_max_value(category: str, categories: list[CategoryDescription]) -> Optional[float]:
    for c in categories:
        if c.name == category:
            return c.max_value
    return None


def get_categorized_transactions_report_df(
    df: pd.DataFrame
) -> dict[str, pd.DataFrame]:
    df['date'] = df.apply(
        lambda r: r['date'].strftime('%d/%m/%Y'),
        axis=1
    )
    df = df.rename({
        'date': 'Date',
        'item': 'Item',
        'value': 'Value',
        'category': 'Category'
    }, axis=1)

    return {
        'others_categories': df[df['Category'] != 'unknown'],
        'unknown_category': df[df['Category'] == 'unknown']
    }


def get_categories_spent_amount_report_df(
    categories_spent_amount: dict[str, float],
    config: Config
) -> pd.DataFrame:
    return pd.DataFrame({
        'Category': categories_spent_amount.keys(),
        'Spent Amount': categories_spent_amount.values(),
        'Expected Amount': [
            get_category_max_value(c, config.categories) or 'Undefined'
                for c in categories_spent_amount
        ]
    })

def generate_report(analysis: Analysis, config: Config, version: str):
    info("  - Generating report")
    file_path = f"Invoice Analyzer v{version} - {config.invoice_source.title()} - {datetime.now().strftime('%Y-%b-%d')}.xlsx"

    categorized_transactions_report_df = get_categorized_transactions_report_df(analysis.categorized_transactions)
    categories_spent_amount_report_df = get_categories_spent_amount_report_df(analysis.categories_spent_amount, config)
    dfs_by_sheet_name = {
        'Categorized Transactions': categorized_transactions_report_df['others_categories'],
        'Unknown Transactions': categorized_transactions_report_df['unknown_category'],
        'Categories Spent Amount': categories_spent_amount_report_df
    }

    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        for sheet_name, df in dfs_by_sheet_name.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        workbook = writer.book
        blue_background_format = workbook.add_format(
            {"bg_color": "#EAF0F6"}
        )  # blue cell background color
        for sheet_name, df in dfs_by_sheet_name.items():
            worksheet = writer.sheets[sheet_name]
            worksheet_index = 0, 0, df.shape[0], df.shape[1] - 1
            worksheet.autofilter(*worksheet_index)
            worksheet.conditional_format(
                *worksheet_index,
                {
                    "type": "formula",
                    "criteria": "=MOD(ROW(),2)=0",
                    "format": blue_background_format,
                },
            )

            worksheet.freeze_panes(1, 0)

            max_size_with_breakline = lambda s: max([len(x) for x in s.split("\n")])
            for idx, col in enumerate(df):
                series = df[col]
                max_len = cast(
                    int,
                    max(
                        (
                            series.astype(str).map(max_size_with_breakline).max(),
                            len(str(series.name)),
                        )
                    ),
                )
                col_size = max_len + 2
                worksheet.set_column(
                    idx,
                    idx,
                    col_size,
                    None,
                )
