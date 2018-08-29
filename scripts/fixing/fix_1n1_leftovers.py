"""
Со следнава скрипта се поправаат останатите редици од (1, _, 1) подмножеството, во кое 29 редици се планирани посети, а
4 редици се адхок посети.
"""

import pandas as pd


def set_ad_hoc(row):
    row['PerformanceEvaluationPlanned'] = ' '


def set_planned(row):
    row['PerformanceEvaluationAdHoc'] = ' '
    row['PerformanceEvaluationExecuted'] = '1'


def edit_row(row, df_rows):
    df_row_number = row['XLS_RowNumber'] - 2
    print('Fixing row with row number {}'.format(df_row_number))
    df_row = df_rows[df_row_number]

    if row['Planned / Ad-Hoc'] == 'Planned':
        set_planned(df_row)
    else:
        set_ad_hoc(df_row)


if __name__ == '__main__':
    df = pd.read_csv('../../data/dataset/Spenser_1_7_7_changed_11n_markers.tsv', sep='\t')
    subset = pd.read_csv('../../data/subsets/ProblematicDataInSpenser_1_7_7/1_n_1_possible_interpretations.tsv',
                         sep='\t')

    df_rows = [row[1] for row in df.iterrows()]
    subset_rows = [row[1] for row in subset.iterrows()]

    for row in subset_rows:
        edit_row(row, df_rows)

    df_fixed = pd.DataFrame(data=df_rows)
    df_fixed.to_csv('../../data/dataset/Spenser_1_7_8_fixed_1n1_leftovers.tsv', sep='\t', index=None)
