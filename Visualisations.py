import matplotlib as mpl
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn import tree
from IPython.display import Image, display
import pydotplus
from scipy import misc
df = pd.read_csv("DataFrame0")
df1 = pd.read_csv("DataFrame1")
df2 = pd.read_csv("DataFrame2")
mvp_df = pd.read_csv("All Time MVP's")
dfs = [df,df1,df2]
# Convert the 'Player' column to a string
df['Player'] = df['Player'].astype(str)
df1['Player'] = df1['Player'].astype(str)
df2['Player'] = df2['Player'].astype(str)
avg_ppg = mvp_df['Points Per Game (PPG)'].mean()


def renderTree(my_tree, features):
    # hacky solution of writing to files and reading again
    # necessary due to library bugs
    filename = "temp.dot"
    with open(filename, 'w') as f:
        f = tree.export_graphviz(my_tree,
                                 out_file=f,
                                 feature_names=features,
                                 class_names=["Dead", "Survived"],
                                 filled=True,
                                 rounded=True,
                                 special_characters=True)

    dot_data = ""
    with open(filename, 'r') as f:
        dot_data = f.read()

    graph = pydotplus.graph_from_dot_data(dot_data)
    image_name = "temp.png"
    graph.write_png(image_name)
    display(Image(filename=image_name))



for df in dfs:
    sns.heatmap(df._get_numeric_data().corr())
    plt.show()
# for df in dfs:
#     filtered_df = df[df['Points Per Game (PPG)'] > avg_ppg]
#     plt.scatter(filtered_df['Player'], filtered_df['Points Per Game (PPG)'])
#     plt.suptitle(df.at[0, 'year'])
#     plt.tick_params(axis='x', labelsize=7)
#     plt.show()

decisionTree = tree.DecisionTreeClassifier()