"""
Следнава скрипта ги поправа неконзистентните записи од подмножеството 1_1_1 (PerformanceEvaluation (Planned, Executed,
AdHoc)). За овие записи забележано е дека евалуацијата е планирана и извршена, а извршена е и адхок посета, но постои
само еден SAPE коефициент.
Прашањето е дали во даден запис, обележан со (1, 1, 1), се работи за планирана или ад-хок посета?
Решението е со пронаоѓање на шаблонот на планирани посети на комерцијалистот. Доколку датумот на посетата влегува во
шаблонот на планирани посети на комерцијалистот, тогаш се работи за планирана посета (1, 1, _), во спротивно се работи
за адхок посета (1, _, 1).
"""

import pandas as pd


def set_ad_hoc(row):
    row['PerformanceEvaluationExecuted'] = ' '


def set_planned(row):
    row['PerformanceEvaluationAdHoc'] = ' '


def edit_row(row, df_rows):
    df_row_number = row['XLS_RowNumber'] - 2
    print('Fixing row with row number {}'.format(df_row_number))
    df_row = df_rows[df_row_number][1]

    if row['Planned / Ad-Hoc'] == 'Planned':
        set_planned(df_row)
    else:
        set_ad_hoc(df_row)


def main():
    df = pd.read_csv('../../data/dataset/Spenser_1_7_3_fixed_nnn_inconsistencies.tsv', sep='\t')
    df_solutions = pd.read_csv('../../data/subsets/ProblematicDataInSpesner_1_7_3/1_1_1_solutions.tsv', sep='\t')

    df_rows = list(df.iterrows())
    df_solutions_rows = list(df_solutions.iterrows())

    for row in df_solutions_rows:
        edit_row(row[1], df_rows)

    df_fixed = pd.DataFrame(data=[row[1] for row in df_rows])
    df_fixed.to_csv('../../data/dataset/Spenser_1_7_4_fixed_111_inconsistencies.tsv', sep='\t', index=None)


if __name__ == '__main__':
    main()
