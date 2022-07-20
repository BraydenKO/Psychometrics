from re import M
from reader import df
from labels import factors
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import sklearn.preprocessing as pp
from sklearn.cluster import KMeans
from matplotlib import colors as mcolors
from sklearn.metrics import silhouette_score

mink = 2
maxk = 16

colormap = np.array(list(dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS).keys()))

def organize_data(df):
    ranges = list(factors.values())
    data = df.iloc[:,ranges[0][0]:ranges[-1][-1]]

    data = data.dropna()
    data = data[data.ne(0).all(1)]
    data = data[data.ne(6).all(1)]
    return data

def reduce(data, dim = 10):
    pca = PCA(n_components=dim)
    pca.fit(data)
    data_p = pca.transform(data)
    return data_p

def optimal_k(data, mink=2, maxk=50, plot = False):
    highscore = 0
    for k in range(mink, maxk+1):
        kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
        label = kmeans.labels_
        score = silhouette_score(data, label, metric = 'euclidean')
        print(f"Score of {score} for k = {k}")
        if score > round(highscore,3):
            highscore = score
            num = k
            best_label = label
    if plot:
        data = reduce(data,dim=2)
        plt.figure()
        plt.scatter(data[:,0], data[:,1], c=colormap[best_label])
        plt.show()
    else:
        return num

def run(data, k):
    kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
    #label of each point
    label = kmeans.labels_
    data = reduce(data, dim=2)
    score = silhouette_score(data, label, metric = 'euclidean')
    print(f"Score of {score}")
    plt.figure()
    plt.scatter(data[:,0], data[:,1], c=colormap[label])

    plt.show()

data = organize_data(df)
data_p = reduce(data, dim=10)
print(optimal_k(data, mink, maxk, plot=True))
