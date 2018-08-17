"""
Следнава скрипта ги поправа неконзистентните записи од подмножеството 1_1_1 (PerformanceEvaluation (Planned, Executed,
AdHoc)). За овие записи забележано е дека евалуацијата е планирана и извршена, а извршена е и адхок посета, но постои
само еден SAPE коефициент.
Решението е да се замени маркерот за PerformanceEvaluationAdHoc од '1' во ' ', односно да се земе дека извршена е само
планираната евалуација од страна на комерцијалистот.
"""

import pandas as pd


def fix_row(row, df_rows):
    df_row_number = row['XLS_RowNumber'] - 2
    print('Fixing row with row number {}'.format(df_row_number))
    df_row = df_rows[df_row_number][1]
    df_row['PerformanceEvaluationAdHoc'] = ' '
    return True


def main():
    df = pd.read_csv('../../data/dataset/Spenser_1_7_3_fixed_nnn_inconsistencies.tsv', sep='\t')
    df_subset = pd.read_csv('../../data/subsets/ProblematicDataInSpesner_1_7_3/1_1_1.tsv', sep='\t')

    df_subset_rows = list(df_subset.iterrows())
    df_rows = list(df.iterrows())

    for row in df_subset_rows:
        ret = fix_row(row[1], df_rows)
        if not ret:
            print(row[1]['XLS_RowNumber'])

    df_fixed = pd.DataFrame(data=[row[1] for row in df_rows])
    df_fixed.to_csv('../../data/dataset/Spenser_1_7_4_fixed_111_inconsistencies.tsv', sep='\t', index=None)


if __name__ == '__main__':
    main()
