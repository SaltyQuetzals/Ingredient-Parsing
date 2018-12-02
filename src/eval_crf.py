import pandas as pd

from sklearn.metrics import classification_report
TRUTH_COLS = ["name", "qty", "range_end", "unit", "comment"]
PRED_COLS = ['pred_' + c for c in TRUTH_COLS]
MATCH_COLS = [c + '_match' for c in TRUTH_COLS]
dtypes = {key: str for key in TRUTH_COLS + PRED_COLS}


def main():
    df = pd.read_csv('../data/eval.csv', keep_default_na=False, dtype=dtypes)
    truth = df[TRUTH_COLS]
    predictions = df[PRED_COLS]
    for t_key, p_key in zip(TRUTH_COLS, PRED_COLS):
        new_col = t_key + '_match'
        df[new_col] = df.apply(
            lambda x: x[t_key].lower() == x[p_key].lower(), axis=1)

    accuracies = df[MATCH_COLS].sum().divide(len(df)).multiply(100)
    print(accuracies)
    print(f'{accuracies.mean()}% accuracy')


if __name__ == "__main__":
    main()
