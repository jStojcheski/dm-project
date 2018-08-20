"""
Оваа скрипта ги поправа неправилностите кои што останаа по поправањето на неконзистентностите од подмножеството 11n.
Записите кои останаа се неправилни поради тоа што за нив е забележано дека евалуацијата е планирана и реализирана, но
недостасува SAPE коефициент. Постојат 130 вакви записи и за нив ќе се се смени маркерот за атрибутот
PerformanceEvaluationExecuted од '1' во ' '.
"""

import pandas as pd
import numpy as np


def get_fpe_coefficient(start, end, df_rows):
    i = start
    fpe = np.nan
    while np.isnan(fpe) and i <= end:
        fpe = df_rows[i][1]['FPECoeficient']
        i += 1
    return fpe


def calculate_sape_coefficient(start, end, df_rows):
    """
    SAPE коефициентот се добива така што се решава равенката (sape_1 + sape_2 + ... + x + ... + sape_n)/n = fpe по x,
    каде што x е непознатиот коефициент (од редицата во која што недостасува SAPE коефициент), а sape_1 ... sape_n се
    останатите евалуации за истиот месец и објект.
    """
    fpe = get_fpe_coefficient(start, end, df_rows)
    if np.isnan(fpe):
        return None, None

    sapes = [df_rows[i][1]['SAPECoeficient'] for i in range(start, end + 1)
             if ~np.isnan(df_rows[i][1]['SAPECoeficient']) and
             ((df_rows[i][1]['PerformanceEvaluationExecuted'] == '1')
              or (df_rows[i][1]['PerformanceEvaluationAdHoc'] == '1'))]
    x = fpe * (len(sapes) + 1) - sum(sapes)
    return x, fpe


def get_range_indices(row_index, rows):
    """
    Почетниот и крајниот индекс се однесуваат на почетниот и крајниот индекс од подмножеството кое го формираат записите
    за даден објект во даден месец.
    """
    month = rows[row_index][1]['month']
    customerID = rows[row_index][1]['CustomerID']

    start, end = row_index, row_index

    # итерирај нанапред за да стигнеш до почетниот индекс
    while rows[start - 1][1]['month'] == month and rows[start - 1][1]['CustomerID'] == customerID:
        start -= 1

    # итерирај наназад за да стигнеш до крајниот индекс
    while rows[end + 1][1]['month'] == month and rows[end + 1][1]['CustomerID'] == customerID:
        end += 1

    return start, end


def fix_row(row, df_rows):
    df_row_number = row['XLS_RowNumber'] - 2
    start, end = get_range_indices(df_row_number, df_rows)

    if start == end == df_row_number:
        # доколку почетниот и крајниот индекс на подмножеството се исти со индексот на редицата која се обработува,
        # тогаш се работи за само еден запис во тој објект за тој месец за кој недостасува SAPE коефициент.
        return False

    sape, fpe = calculate_sape_coefficient(start, end, df_rows)
    if sape is None or fpe is None:
        return False
    df_rows[df_row_number][1]['SAPECoeficient'] = sape
    df_rows[df_row_number][1]['FPECoeficient'] = fpe
    return True


def main():
    df = pd.read_csv('../../data/dataset/Spenser_1_7_4_fixed_111_inconsistencies.tsv', sep='\t')
    df_subset = pd.read_csv('../../data/subsets/ProblematicDataInSpesner_1_7_3/subset_11n.tsv', sep='\t')

    df_rows = list(df.iterrows())
    df_subset_rows = list(df_subset.iterrows())

    unfixed_rows = []

    for row in df_subset_rows:
        ret = fix_row(row[1], df_rows)
        if not ret:
            unfixed_rows.append(row[1])

    df_fixed = pd.DataFrame(data=[row[1] for row in df_rows])
    df_fixed.to_csv('../../data/dataset/Spenser_1_7_5_fixed_11n_leftovers.tsv', sep='\t', index=None)

    df_unfixed = pd.DataFrame(data=unfixed_rows)
    df_unfixed.to_csv('../../data/subsets/ProblematicDataInSpesner_1_7_5/11n_unfixed_rows.tsv', sep='\t', index=None)


if __name__ == '__main__':
    main()
