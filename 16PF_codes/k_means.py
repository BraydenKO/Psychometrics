from re import M
from reader import df
from labels import factors
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
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

def optimal_k(data, mink=2, maxk=50, method = 'silhouette'):
    import matplotlib.style as style
    if method == 'silhouette':
        silhouettes = []
        for k in range(mink, maxk+1):
            kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
            label = kmeans.labels_
            score = silhouette_score(data, label, metric = 'euclidean')
            print(f"{score} : {k}")
            silhouettes.append(score)

        style.use("fivethirtyeight")
        plt.plot(range(mink, maxk+1), silhouettes)
        plt.xlabel("Number of Clusters (k)")
        plt.ylabel("score")
        plt.show()
    
    # Checks specifically for 5 and 16
    elif method == 'silhouette_local_max':
        silhouettes = []
        for k in range(4,7):
            kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
            label = kmeans.labels_
            score = silhouette_score(data, label, metric = 'euclidean')
            print(f"{score} : {k}")
            silhouettes.append(score)
        for k in range(15,18):
            kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
            label = kmeans.labels_
            score = silhouette_score(data, label, metric = 'euclidean')
            print(f"{score} : {k}")
            silhouettes.append(score)
        a = 1 if silhouettes[1] > silhouettes[0] and silhouettes[1] > silhouettes[2] else 0
        b = 1 if silhouettes[4] > silhouettes[3] and silhouettes[4] > silhouettes[5] else 0

        return a, b
    
    elif method == 'elbow':
        inertias=[]
        for k in range(mink, maxk+1):
            kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
            inertias.append(kmeans.inertia_)

        style.use("fivethirtyeight")
        plt.plot(range(mink, maxk+1), inertias)
        plt.xlabel("Number of Clusters (k)")
        plt.ylabel("Distance")
        plt.show()

def run(data, k, display_dim=2):

    kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
    #label of each point
    label = kmeans.labels_
    score = silhouette_score(data, label, metric = 'euclidean')
    print(f"Score of {score}")

    plot(data,display_dim,label)

def run_through_dims(data, mindim, maxdim, mink, maxk):
  for dim in range(mindim, maxdim+1):
    data_p = reduce(data, dim)
    print(f"{dim} dimension with {optimal_k(data_p, mink, maxk)} clusters")

def plot(data, dim,label):
  if dim == 3:
    data = reduce(data,dim=3)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data[:,0], data[:,1], data[:,2], c=colormap[label])
    plt.show()
  elif dim == 2:
    data = reduce(data,dim=2)
    plt.figure()
    plt.scatter(data[:,0], data[:,1], c=colormap[label])
    plt.show()

data = organize_data(df)

#fives, sixteens = 0, 0
#for dim in range(2, 10,1):
#    print(dim)
#    data_p = reduce(data, dim)
#    five, sixteen = optimal_k(data_p, method = 'silhouette_local_max')
#    fives += five
#    sixteens += sixteen

#print(f"five: {fives}\nsixteen: {sixteens}")

'''
Note at k = 5 and 16, you tend to find quite a few local maximums
'''