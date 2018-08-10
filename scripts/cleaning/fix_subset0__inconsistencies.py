# coding=utf-8
import pandas as pd
import numpy as np


def get_end_index(starting_row_id):
    """
    Го враќа индексот на следната редица од тековната за која што важи дека PerformanceEvaluationPlanned e 0
    и PerformanceEvaluationExecuted e ' '.
    """
    for i in range(starting_row_id + 1, len(df_rows)):
        row = df_rows[i][1]
        if row['PerformanceEvaluationPlanned'] == '0' and row['PerformanceEvaluationExecuted'] == ' ':
            return i
    return i


def fix_coefficients(row_1, row_2):
    row_2['SAPECoeficient'] = row_1['SAPECoeficient']
    row_2['FPECoeficient'] = row_1['FPECoeficient']
    row_1['SAPECoeficient'] = np.nan
    row_1['FPECoeficient'] = np.nan


def is_the_right_row(row):
    """
    За оваа редица треба да е забележано дека евалуцијата е планирана и реализирана и да недостасува коефициентот на евалуација.
    """
    return row['PerformanceEvaluationPlanned'] == '1' and row['PerformanceEvaluationExecuted'] == '1' \
           and np.isnan(row['SAPECoeficient'])


def fix_row(row):
    df_row_id = row['XLS_RowNumber'] - 2  # id на редицата од табелата 'Spenser_1_7_remove_v22_threshold.tsv'
    inconsistent_row = df_rows[df_row_id][1]  # редицата во која што е погрешно внесен SAPE коефициент
    end_index = get_end_index(df_row_id)  # крајниот индекс на пребарување

    for i in range(df_row_id + 1, end_index):
        df_row = df_rows[i][1]
        if is_the_right_row(df_row):  # проверка дали ова е редицата во која што треба да се префрлат SAPE и FPE
            # коефициентите
            fix_coefficients(inconsistent_row, df_row)  # префрлање на SAPE и FPE коефициентите од неконзистентната
            # редица во оваа редица
            return True
    # не е пронајдена соодветна редица за замена, значи коефицинетот треба да се избрише?
    return False


if __name__ == '__main__':
    df = pd.read_csv('../../data/dataset/Spenser_1_7_remove_v22_treshold.tsv', sep='\t')
    subset_0__ = pd.read_csv('../../data/subsets/PerformanceEvaluation/0_n_n.tsv', sep='\t')

    # Следнава податочна рамка се состои од записите за кои е забележано дека евалуацијата од страна на комерцијалистот
    # не е планирана, ниту реализирана, а сепак постои внесена вредност за SAPE коефициентот. Оваа вредност треба да се
    # пренесе во следната редица, каде што е забележано дека евалуацијата е планирана и реализирана, но недостасува SAPE
    # коефициентот.

    df_inconsistencies = subset_0__[~np.isnan(subset_0__.SAPECoeficient)]

    subset_rows = list(df_inconsistencies.iterrows())
    df_rows = list(df.iterrows())

    rows_with_no_match = []

    for row in subset_rows:
        ret_flag = fix_row(row[1])
        if not ret_flag:
            rows_with_no_match.append(row[1])

    df_rows_no_indices = [row[1] for row in df_rows]

    df_fixed = pd.DataFrame(df_rows_no_indices)
    df_fixed.to_csv(path_or_buf='../../data/dataset/Spenser_1_7_subset0__fix.tsv', sep='\t', index=None)

    df_rows_with_no_match = pd.DataFrame(rows_with_no_match)  # постојат 4 вакви редици, коефициентите во овие редици
    # ќе бидат отстранети рачно
    df_rows_with_no_match.to_csv('../../data/subsets/rows_with_no_match_fix_subset_00_.tsv', sep='\t', index=None)
