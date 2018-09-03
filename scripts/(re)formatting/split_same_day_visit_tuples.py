import pandas as pd
import numpy as np


def delete_same_day_visit_value(index, df_rows):
    row = np.copy(df_rows[index])
    row[11] = ' '
    if row[-2] == 'same day visit':
        row[-2] = ' '
    return row


def construct_new_tuple(index, df_rows):
    row = df_rows[index]

    cust_ID = row[0]
    date = row[1]
    month = row[2]
    pe_planned, pe_executed, pe_adhoc = ' ', ' ', ' '  # кодирањето на PE атрибутите за екстерна евалуација
    terr_ID = row[6]
    sales_group = row[7]
    sape = np.nan
    ape = row[9]
    fpe = np.nan
    sdv = 'same day visit'
    overdue = ' '
    underdue = ' '
    ok = ' '
    not_ok = ' '
    status = ' '
    overdue_days = ' '

    new_tuple = np.array([cust_ID, date, month, pe_planned, pe_executed, pe_adhoc, terr_ID, sales_group,
                          sape, ape, fpe, sdv, overdue, underdue, ok, not_ok, status, overdue_days], dtype=object)

    return new_tuple


def split_row(index, df_rows):
    external_eval_tup = construct_new_tuple(index, df_rows)
    row = np.copy(df_rows[index])
    row[9] = np.nan
    return row, external_eval_tup


def process_row(index, df_rows):
    row = df_rows[index]

    if row[11] != 'same day visit':
        return [row]

    if np.isnan(row[8]):
        fixed_row = delete_same_day_visit_value(index, df_rows)
        return [fixed_row]

    orig_tuple_fixed, eval_tuple = split_row(i, df_rows)
    return [orig_tuple_fixed, eval_tuple]


if __name__ == '__main__':
    df = pd.read_csv('../../data/dataset/Spenser_1_7_8_fixed_1n1_leftovers.tsv', sep='\t')
    df_rows = df.values

    new_df_rows = []

    for i in range(len(df_rows)):
        ret = process_row(i, df_rows)
        new_df_rows.extend(ret)

    new_df = pd.DataFrame(data=new_df_rows, columns=df.columns)
    new_df.to_csv('../../data/dataset/Spenser_1_7_9_split_same_day_visit_tuples.tsv', sep='\t', index=None)
