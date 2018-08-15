import pandas as pd

"""
Кодот е превземен од тетратката 'notebooks/02_extract_performance_evaluation_subsets.ipynb'
Промени го името на фајлот во првата линија и името на фолдерот во последната линија ако оваа скрипта се пушта на друго
податочно множество.
"""

if __name__ == '__main__':

    df = pd.read_csv('../../data/dataset/Spenser_1_7_1_fixed_0nn_inconsistencies.tsv', sep='\t')
    df.index = pd.RangeIndex(start=2, stop=len(df) + 2)
    df.index.name = 'XLS_RowNumber'

    s = set(tuple([i[3], i[4], i[5]])
            for i in list(df.values))
    s = sorted(list(s))

    for i in s:
        p, e, a = i
        t = df[(df.PerformanceEvaluationPlanned == p) &
               (df.PerformanceEvaluationExecuted == e) &
               (df.PerformanceEvaluationAdHoc == a)]
        p = 'n' if p == ' ' else p
        e = 'n' if e == ' ' else e
        a = 'n' if a == ' ' else a
        t.to_csv('../../data/subsets/PerformanceEvaluationOnSpenser_1_7_1/{}_{}_{}.tsv'.format(p, e, a), sep='\t')
