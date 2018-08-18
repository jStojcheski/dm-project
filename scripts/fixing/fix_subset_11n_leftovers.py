"""
Оваа скрипта ги поправа неправилностите кои што останаа по поправањето на неконзистентностите од подмножеството 11n.
Записите кои останаа се неправилни поради тоа што за нив е забележано дека евалуацијата е планирана и реализирана, но
недостасува SAPE коефициент. Постојат 130 вакви записи и за нив ќе се се смени маркерот за атрибутот
PerformanceEvaluationExecuted од '1' во ' '.
"""

import pandas as pd


def fix_row(row, df_rows):
    df_row_number = row['XLS_RowNumber'] - 2
    print('Fixing row with row number {}'.format(df_row_number))
    df_row = df_rows[df_row_number][1]
    df_row['PerformanceEvaluationExecuted'] = ' '


def main():
    df = pd.read_csv('../../data/dataset/Spenser_1_7_4_fixed_111_inconsistencies.tsv', sep='\t')
    df_subset = pd.read_csv('../../data/subsets/ProblematicDataInSpesner_1_7_3/subset_11n.tsv', sep='\t')

    df_rows = list(df.iterrows())
    df_subset_rows = list(df_subset.iterrows())

    for row in df_subset_rows:
        fix_row(row[1], df_rows)

    df_fixed = pd.DataFrame(data=[row[1] for row in df_rows])
    df_fixed.to_csv('../../data/dataset/Spenser_1_7_5_fixed_11n_leftovers.tsv', sep='\t', index=None)


if __name__ == '__main__':
    main()
