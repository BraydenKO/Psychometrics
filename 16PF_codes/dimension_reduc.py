from reader import df
from labels import factors
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

def organize_data(df):
    ranges = list(factors.values())
    data = df.iloc[:,ranges[0][0]:ranges[-1][-1]]

    data = data.dropna()
    data = data[data.ne(0).all(1)]
    data = data[data.ne(6).all(1)]
    return data

def optimal(data):
    pca = PCA(n_components=len(data.columns))
    pca.fit(data)
    #data_p = pca.transform(data)
    plt.plot(np.cumsum(pca.explained_variance_ratio_ * 100))
    plt.xlabel("Number of Components")
    plt.ylabel("Explained Variance")
    plt.show()

def reduce(data, dim = 10):
    pca = PCA(n_components=dim)
    pca.fit(data)
    data_p = pca.transform(data)
    return data_p