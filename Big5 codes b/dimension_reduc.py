'''
Find optimal number of dimensions to reduce
data to using the elbow method and perumations method
'''
from reader import df, pd
from labels import factors
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

def organize_data(df):
  """
  Organizes data to get rid of unused columns
  and rows with invalid data (na, 0, 6).

  df: pandas DataFrame

  returns:
  data: Organized and normalized dataset (numpy array)
  """
  from sklearn.preprocessing import MinMaxScaler
  # Collects just questionaire data
  ranges = list(factors.values())
  data = df.iloc[:,ranges[0][0]:ranges[-1][-1]]

  # Deletes people with NaN, 0, or a 6 in their answer
  # 0 or 6 means a skipped question
  data = data.dropna()
  data = data[data.ne(0).all(1)]
  data = data[data.ne(6).all(1)]

  # Scale data between 0 and 1
  # Note: I dont know how useful this is considering that
  # All the data is at the same scale 1-5 anyways but I 
  # See people do this all the time and it can't hurt.
  scaler = MinMaxScaler(feature_range=(0,1))
  data = scaler.fit_transform(data)
  
  return data

def find_elbow(x,y, curve = 'concave', direction = 'increasing'):
  """Finds an elbow using kneed.KneeLocator
  
  x: x values of line (array)
  y: y values of line (array)
  curve: 'concave' or 'convex' (refer to kneed docs) (str)
  direction: 'increasing' or 'decreasing' (refer to kneed docs) (str)

  returns:
  kn: KneeLocator object from kneed
  """
  from kneed import KneeLocator
  kn = KneeLocator(x, y, curve=curve, direction=direction)
  return kn

def optimal(data, method = 1):
  """
  Find optimal number of dimensions to decrease to.
  
  data: Dataset to analyze
  method: If method == 1 (default) use elbow method, 
    if method == 2 use permuations test method
  """
  assert method == 1 or method == 2, f"Method must equal 1 (elbow) or 2 (permutations), you entered {method}"
  # Returns 12
  if method == 1:
    pca = PCA().fit(data)
    print(pca.explained_variance_ratio_)
    y = np.cumsum(pca.explained_variance_ratio_ * 100)
    x = range(1,len(y)+1)
    plt.plot(x,y)
    kn =find_elbow(x,y)
    knee = kn.knee
    plt.axvline(x = knee, ymax = np.interp(knee,x,y), label = knee, color = 'k')
    plt.legend()
    plt.xlabel("Number of Components")
    plt.ylabel("Explained Variance")
    plt.show()

  # returns 6
  elif method == 2:
    import plotly.graph_objects as go
    def de_correlate_df(df):
      X_aux = df.copy()
      for col in df.columns:
        X_aux[col] = df[col].sample(len(df)).values
      
      return X_aux

    pca = PCA()
    pca.fit(data)
    original_variance = pca.explained_variance_ratio_
    N_permutations = 100
    variance = np.zeros((N_permutations, len(data.columns)))
    for i in range(N_permutations):
      X_aux = de_correlate_df(data)
      pca.fit(X_aux)
      variance[i, :] = pca.explained_variance_ratio_
    p_val = np.sum(variance > original_variance, axis=0) / N_permutations

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[f'PC{i}' for i in range(len(data.columns))], y=p_val, name='p-value on significance'))
    fig.update_layout(title="PCA Permutation Test p-values")
    fig.show()

def reduce(data, dim = 10):
  """
  Reduces a dataset to a lower number of dimensions using 
  sklearn.decomposition.PCA

  data: Dataset to lower in dimensionality (2d array)
  dim: Number of dimensions to reduce to (default 10) (int)

  returns:
  data_r: Data with reduced dimensionality (2d array)
  """
  pca = PCA(n_components=dim)
  pca.fit(data)
  data_p = pca.transform(data)
  return data_p

if __name__ == "__main__":
  data = organize_data(df)
  data = pd.DataFrame(data)
  optimal(data, method = 1)
  optimal(data, method = 2)