import pandas as pd
from tabulate import tabulate
df = pd.read_csv("DataFrame0")
print(tabulate(df, headers='keys'))
df = pd.read_csv("DataFrame1")
print(tabulate(df, headers='keys'))
df = pd.read_csv("DataFrame2")
print(tabulate(df, headers='keys'))

