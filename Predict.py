import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tabulate import tabulate
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import cross_val_score
import sklearn
from sklearn.ensemble import RandomForestClassifier
result = pd.read_csv("result")
del result['Unnamed: 0']

# split to train and test using only the numeric columns
X_train,X_test,y_train,y_test = train_test_split(result[['Victories in Season','Team Conference Rank','Minutes Per Game','Is All-Star']],result['MVP Prospect'],random_state=42,test_size=0.3)

clf = DecisionTreeClassifier(max_depth=4, min_samples_split=20)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print("Predicted labels:\n", y_pred)
print("Actual labels:\n", y_test.values)
print(acc)

y_pred_padded = np.pad(y_pred, (0, result.shape[0]-y_pred.shape[0]), 'constant')
df_y_pred = pd.DataFrame({'Player': result['Player'], 'y_pred': y_pred_padded})
player_names = df_y_pred.loc[df_y_pred['y_pred'] == 1, 'Player']
print(player_names)

print(len(y_pred))
# print(tabulate(result, headers='keys'))
