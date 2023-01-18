import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tabulate import tabulate
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import cross_val_score
import sklearn
from sklearn.ensemble import RandomForestClassifier
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
    df['MVP Prospect'].fillna(0, inplace=True)
    # print('\n\n\n')
result = pd.concat([df1,df2])
result.dropna(how="any",inplace=True)
# select only the numeric columns
numeric_cols = result.select_dtypes(include=['float64','int64']).columns

# split to train and test using only the numeric columns
X_train,X_test,y_train,y_test = train_test_split(result[['Victories in Season','Team Conference Rank','Points Per Game (PPG)','Minutes Per Game']],result['MVP Prospect'],random_state=42,test_size=0.2)

clf = DecisionTreeClassifier(max_depth=4, min_samples_split=10)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print("Predicted labels:\n", y_pred)
print("Actual labels:\n", y_test.values)
print(acc)


y_pred_padded = np.pad(y_pred, (0, df.shape[0]-y_pred.shape[0]), 'constant')
df_y_pred = pd.DataFrame({'Player': df['Player'], 'y_pred': y_pred_padded})
player_names = df_y_pred.loc[df_y_pred['y_pred'] == 1, 'Player']
print(player_names)
# print(tabulate(result, headers='keys'))