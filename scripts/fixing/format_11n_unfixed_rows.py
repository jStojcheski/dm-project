"""
Со следнава скрипта, остатоците од непоправените редици во подмножеството 11n ќе бидат форматирани, односно маркерите за
(PEP, PEE и PEAH) ќе бидат поставени на (1, 0, 0).
"""

import pandas as pd


def main():
    df = pd.read_csv('../../data/dataset/Spenser_1_7_6_fixed_nn1_leftovers.tsv', sep='\t')
    df_subset = pd.read_csv('../../data/subsets/ProblematicDataInSpesner_1_7_6/11n_unfixed_rows.tsv', sep='\t')

    df_rows = [row[1] for row in df.iterrows()]
    subset_rows = [row[1] for row in df_subset.iterrows()]

    for row in subset_rows:
        row_id = row['XLS_RowNumber'] - 2
        df_row = df_rows[row_id]
        df_row['PerformanceEvaluationExecuted'] = '0'
        df_row['PerformanceEvaluationAdHoc'] = '0'

    df_fixed = pd.DataFrame(data=df_rows)
    df_fixed.to_csv('../../data/dataset/Spenser_1_7_7_changed_11n_markers.tsv', sep='\t', index=None)


if __name__ == '__main__':
    main()
