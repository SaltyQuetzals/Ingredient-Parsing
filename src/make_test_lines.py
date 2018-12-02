import pandas as pd

def main():
    df = pd.read_csv('../data/test.csv')
    with open('../test_lines.txt', 'w+') as f:
        f.write('\n'.join(df['input'].tolist()))

if __name__ == "__main__":
    main()