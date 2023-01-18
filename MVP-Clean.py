import pandas as pd
from tabulate import tabulate
df = pd.read_csv("DataFrame0")
df1 = pd.read_csv("DataFrame1")
df2 = pd.read_csv("DataFrame2")
dfs = [df,df1,df2]
for df in dfs:
    del df['Unnamed: 0']
    df.dropna(subset=['Player'], how='all', inplace=True)
    df.dropna(subset=['Victories in Season'], how='all', inplace=True)
    df['Won Conference'].fillna(0, inplace=True)
    df['Is All-Star'].fillna(0, inplace=True)
    print(tabulate(df, headers='keys'))

