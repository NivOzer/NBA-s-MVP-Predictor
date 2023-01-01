import pandas as pd
from tabulate import tabulate
df = pd.read_csv("DataFrame0")
print(tabulate(df, headers='keys'))
df1 = pd.read_csv("DataFrame1")
print(tabulate(df1, headers='keys'))
