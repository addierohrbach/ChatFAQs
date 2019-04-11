import openpyxl
from collections import defaultdict


def import_data():
    wb = openpyxl.load_workbook("data/faqs.xlsx")
    ws = wb.worksheets[0]
    faq_table = defaultdict(dict)

    for row in ws.iter_rows(min_row=1, max_col=2):
        question, answer = (c.value for c in row)
        if question not in faq_table:
            faq_table[question] = answer

    print(faq_table)

import_data()