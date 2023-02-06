from tabulate import tabulate
import pandas as pd
df = pd.read_csv("DataFrame0")
df1 = pd.read_csv("DataFrame1")
df2 = pd.read_csv("DataFrame2")
dfs = [df,df1,df2]
#Cleaning Phase
for df in dfs:
    del df['Unnamed: 0']
    df.dropna(subset=['Player'], how='all', inplace=True)
    df.dropna(subset=['Victories in Season'], how='all', inplace=True)
    df['Won Conference'].fillna(0, inplace=True)
    df['Is All-Star'].fillna(0, inplace=True)
    df['MVP Prospect'].fillna(0, inplace=True)
    # df['MVP Prospect'] = df['Points Per Game (PPG)'].apply(lambda x: 1 if x > 27 else 0)
    # df['MVP Prospect'] = df['Defensive Rebounds Per Game (DRPG)'].apply(lambda x: 1 if x >=7 else 0)
    # df['MVP Prospect'] = df['Blocks'].apply(lambda x: 1 if x >=0.6 else 0)
    df['MVP Prospect'] = df[['Points Per Game (PPG)', 'Defensive Rebounds Per Game (DRPG)', 'Blocks']].apply(lambda x: 1 if (x['Points Per Game (PPG)'] >= 27) | (x['Defensive Rebounds Per Game (DRPG)'] >= 6) | (x['Blocks'] >= 0.6) else 0, axis=1)
result = pd.concat([df,df1,df2])

result.dropna(how="any",inplace=True)
# select only the numeric columns
numeric_cols = result.select_dtypes(include=['float64','int64']).columns
result.to_csv("result")

print(tabulate(result, headers='keys'))