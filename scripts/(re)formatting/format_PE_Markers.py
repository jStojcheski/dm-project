"""
Со следнава скрипта се постигнува нов формат на трите атрибути за Performance Evaluation. Деталите за новото форматирање
се дадени во Табела 2 од документот на Drive.
Воедно, во оваа скрипта се менува и типот на вредностите кај овие три атрибути од str во int.
"""

import os

import pandas as pd


def to_000(subset, df_rows):
    for row in subset:
        df_row_id = row['XLS_RowNumber'] - 2
        df_row = df_rows[df_row_id]
        df_row['PerformanceEvaluationPlanned'] = '0'
        df_row['PerformanceEvaluationExecuted'] = '0'
        df_row['PerformanceEvaluationAdHoc'] = '0'


def to_100(subset, df_rows):
    for row in subset:
        df_row_id = row['XLS_RowNumber'] - 2
        df_row = df_rows[df_row_id]

        df_row['PerformanceEvaluationPlanned'] = '1'
        df_row['PerformanceEvaluationExecuted'] = '0'
        df_row['PerformanceEvaluationAdHoc'] = '0'


def to_110(subset, df_rows):
    for row in subset:
        df_row_id = row['XLS_RowNumber'] - 2
        df_row = df_rows[df_row_id]

        df_row['PerformanceEvaluationPlanned'] = '1'
        df_row['PerformanceEvaluationExecuted'] = '1'
        df_row['PerformanceEvaluationAdHoc'] = '0'


def to_010(subset, df_rows):
    for row in subset:
        df_row_id = row['XLS_RowNumber'] - 2
        df_row = df_rows[df_row_id]

        df_row['PerformanceEvaluationPlanned'] = '0'
        df_row['PerformanceEvaluationExecuted'] = '1'
        df_row['PerformanceEvaluationAdHoc'] = '0'


def to_001(subset, df_rows):
    for row in subset:
        df_row_id = row['XLS_RowNumber'] - 2
        df_row = df_rows[df_row_id]

        df_row['PerformanceEvaluationPlanned'] = '0'
        df_row['PerformanceEvaluationExecuted'] = '0'
        df_row['PerformanceEvaluationAdHoc'] = '1'


def fix_subset(subset_filename, subset_rows, df_rows):
    if subset_filename == '0_n_1.tsv':
        to_010(subset_rows, df_rows)

    elif subset_filename == '0_n_n.tsv':
        to_000(subset_rows, df_rows)

    elif subset_filename == '1_0_0.tsv':
        to_100(subset_rows, df_rows)

    elif subset_filename == '1_1_n.tsv':
        to_110(subset_rows, df_rows)

    elif subset_filename == '1_n_n.tsv':
        to_100(subset_rows, df_rows)

    elif subset_filename == 'n_n_1.tsv':
        to_010(subset_rows, df_rows)

    elif subset_filename == 'n_n_n.tsv':
        to_001(subset_rows, df_rows)


if __name__ == '__main__':
    df = pd.read_csv('../../data/dataset/Spenser_1_7_9_split_same_day_visit_tuples.tsv', sep='\t')
    list_of_subsets = list(os.walk('../../data/subsets/PerformanceEvaluationOnSpenser_1_7_9'))[0][2]

    df_rows = [row[1] for row in df.iterrows()]

    for subset_filename in list_of_subsets:
        subset_path = os.path.join('../../data/subsets/PerformanceEvaluationOnSpenser_1_7_9', subset_filename)
        df_subset = pd.read_csv(subset_path, sep='\t')
        subset_rows = [row[1] for row in df_subset.iterrows()]
        fix_subset(subset_filename, subset_rows, df_rows)

    new_columns = list(df.columns)
    new_columns[5] = 'ExternalEvaluation'

    df = pd.DataFrame(data=df_rows)

    df_fixed = pd.DataFrame(data=df_rows, columns=new_columns)
    df_fixed['ExternalEvaluation'] = df['PerformanceEvaluationAdHoc']

    df_fixed['PerformanceEvaluationPlanned'] = pd.Series([int(val) for val in df_fixed['PerformanceEvaluationPlanned']])
    df_fixed['PerformanceEvaluationExecuted'] = pd.Series(
        [int(val) for val in df_fixed['PerformanceEvaluationExecuted']])
    df_fixed['ExternalEvaluation'] = pd.Series([int(val) for val in df_fixed['ExternalEvaluation']])

    df_fixed.to_csv('../../data/dataset/Spenser_1_8_new_format_on_PE_markers.tsv', sep='\t', index=None)
