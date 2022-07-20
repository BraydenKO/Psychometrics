
from reader import df
from labels import factors
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

ranges = list(factors.values())
data = df.iloc[:,ranges[0][0]:ranges[-1][-1]]

data = data.dropna()
data = data[data.ne(0).all(1)]
data = data[data.ne(6).all(1)]

def optimal(data):
    pca = PCA(n_components=len(data.columns))
    pca.fit(data)
    #data_p = pca.transform(data)
    plt.plot(np.cumsum(pca.explained_variance_ratio_ * 100))
    plt.xlabel("Number of Components")
    plt.ylabel("Explained Variance")
    plt.show()

optimal(data)