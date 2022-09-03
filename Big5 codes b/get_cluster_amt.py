'''
Filled with tools to analyze how many clusters appear in the data
'''
import matplotlib.pyplot as plt
from reader import df, pd
from labels import factors
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

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
  data = df.iloc[:,ranges[0][0]:ranges[-1][-1]+1]

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

def moving_average(data, window):
  """Returns the moving average to smooth out data.
  
  data: Dataset to smooth (1d array)
  window: Window to look at for the moving average
  
  returns:
  new_data: Smoothed out data (1d array)
  """
  new_data = []
  for idx in range(len(data)):
    if idx < window:
      new_data.append(sum(data[:idx+1])/len(data[:idx+1]))
    else:
      new_data.append(sum(data[idx-window:idx+1])/len(data[idx-window:idx+1]))
  return new_data

def plot(data, dim,label):
  """
  plots clusters in 2 or 3 dimensions and colors
  them based on label
  
  data: Dataset to plot
  dim: Number of dimensions to display in (2 or 3) (int)
  label: Specifies the clusters and how to color them (array)
  """

  import matplotlib.colors as mcolors
  colormap = np.array(list(dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS).keys()))
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

def run_k_means(data, k, dim=2, show = True):
  """
  Runs kmeans clustering  on a given dataset with a set k amount of 
  clusters.
  
  data: Dataset to apply kmeans to (array or DataFram)
  k: Number of clusters (int)
  show: Whether to display the clusters visually with plot(data,dim,label) (bool)
  dim: Number of dimensions to display clusters in if show == True (default 2) (int)
  
  returns:
  kmeans: KMeans object from sklearn
  """

  kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
  label = kmeans.fit_predict(data)
  if show:
    plot(data,dim,label)
  return kmeans

def norm_list(data):
  """Fits data in list between 0 and 1
  
  data: 1d array to fit
  
  returns:
  scaled: 1d array of scaled data
  """

  minimum = min(data)
  maximum = max(data)
  scaled = []
  for i in data:
    scaled.append((i - minimum) / (maximum - minimum))
  return scaled

def Hopkins(data, samples = None):
  """Runs the Hopkins statistic from pyclustertend. Refer to their docs.
  
  data: Dataset to analyze
  samples: Number of samples to look at. If None (default) look at all rows (int or None)
  
  returns:
  float representing Hopkins statistic score.
  """

  from pyclustertend import hopkins
  if samples == None:
    return hopkins(data, len(data))
  else:
    return hopkins(data, samples)

def standard_error(data):
  """Returns the standard error of a list"""

  n = len(data)
  mean = sum(data)/n
  deviations_sqr = []
  for value in data:
    deviations_sqr.append((mean-value)**2)
  
  std = (sum(deviations_sqr)/(n-1))**(1/2)
  ste = std/(n**(1/2))
  return ste
'''
(note has f'(x)>0 and f''(x) <0 shape- this could affect methods that use max(Gap(k)))
In ~50 dim k = 7 by the Gap(k) >= Gap(k+1) - Se
In ~50 dim k = max(k) by max(Gap(k))

(note has a hill shape)
In    6 dim k = 4 by Gap(k) >= Gap(k+1) - Se
In    6 dim k = 5 by max(Gap(k))
In    6 dim k = 4 by the Gap(k) >= max(Gap(k)) - Se

(note has f'(x)>0 and f''(x) <0 shape- this could affect methods that use max(Gap(k)))
In   12 dim k = 7 by Gap(k) >= Gap(k+1) - Se
In   12 dim k = 39 or 27 by max(Gap(k))
In   12 dim k =  19 or 14 by the Gap(k) >= max(Gap(k)) - Se
'''
def GapStat(data, nrefs=3, maxClusters=15):
  """
  Calculates KMeans optimal K using Gap Statistic 

  data: Dataset to analyze (2d array)
  nrefs: Number of sample reference datasets to create
  maxClusters: Maximum number of clusters to test
  
  returns:
  The k values for highest gap
  resultsdf: The gap values for each tested k value
  """
  gaps = np.zeros((len(range(1, maxClusters)),))
  resultsdf = pd.DataFrame({'clusterCount':[], 'gap':[]})
  for gap_index, k in enumerate(range(1, maxClusters)):
    print(k)
# Holder for reference dispersion results
    refDisps = np.zeros(nrefs)
# For n references, generate random sample and perform kmeans getting resulting dispersion of each loop
    for i in range(nrefs):        
      # Create new random reference set
      randomReference = np.random.random_sample(size=data.shape)
      
      # Fit to it
      km = KMeans(k)
      km.fit(randomReference)
      
      refDisp = km.inertia_
      refDisps[i] = refDisp
# Fit cluster to original data and create dispersion
    km = KMeans(k)
    km.fit(data)
    
    origDisp = km.inertia_
# Calculate gap statistic
    gap = np.log(np.mean(refDisps)) - np.log(origDisp)
# Assign this loop's gap statistic to gaps
    gaps[gap_index] = gap
    
    resultsdf = resultsdf.append({'clusterCount':k, 'gap':gap}, ignore_index=True)
  return (gaps.argmax() + 1, resultsdf)

# No meaningful elbow
def elbow_method (data):
  """
  Uses the elbow method from yellowbrick to calculate
  optimal value of k (refer to their docs).
  """
  from yellowbrick.cluster import KElbowVisualizer
  km = KMeans()
  visualizer = KElbowVisualizer(km, k=(2,30), timings= True)
  visualizer.fit(data)       
  visualizer.show()      

# Max is at 2 but elbow at maybe around 7 but it's ambiguous
def sil_method(data):
  """Uses the silhouette score to calcluate optimal k value
  
  data: Datset to analyze (2d array)
  """

  from sklearn.metrics import silhouette_score

  scores = []
  x = range(2,30)
  for k in x:
    km = KMeans(n_clusters=k)
    print(k)
    scores.append(silhouette_score(data, km.fit(data).labels_))

  plt.plot(x, scores)
  plt.show()

  from yellowbrick.cluster import KElbowVisualizer
  km = KMeans()
  # k is range of number of clusters.
  visualizer = KElbowVisualizer(km, k=(2,30),metric='silhouette', timings= True)
  visualizer.fit(data)        # Fit the data to the visualizer
  visualizer.show()        # Finalize and render the figure

# max is at 2 with an ambiguos elbow
def calinski_harabasz(data):
  """Uses the Calinski Harabasz metric to find optilam k value.
  
  data: 2d Dataset to analyze
  """

  # Import ElbowVisualizer
  from yellowbrick.cluster import KElbowVisualizer
  km = KMeans()
  # k is range of number of clusters.
  visualizer = KElbowVisualizer(km, k=(2,30),metric='calinski_harabasz', timings= True)
  visualizer.fit(data)        # Fit the data to the visualizer
  visualizer.show()        # Finalize and render the figure

# Gives possible optimal values like k = 5 and k = 14
def Davies(data, plot = True):
  """Uses the Davues Bouldin score to get optimal k value.
  
  data: 2d Dataset to analyze
  plot: Whether to make a plot or just return scores

  returns:
  scores (array)
  """

  # Davies Bouldin score for K means
  from sklearn.metrics import davies_bouldin_score
  def get_kmeans_score(data, center):
    '''
    returns the kmeans score regarding Davies Bouldin for points to centers
    
    data: The dataset you want to fit kmeans to
    center: The number of centers you want (the k value)
    
    returns:
    score: The Davies Bouldin score for the kmeans model fit to the data
    '''
    #instantiate kmeans
    kmeans = KMeans(n_clusters=center)
# Then fit the model to your data using the fit method
    model = kmeans.fit_predict(data)
    
    # Calculate Davies Bouldin score
    score = davies_bouldin_score(data, model)
    
    return score

  scores = []
  centers = list(range(2,40))
  for center in centers:
      scores.append(get_kmeans_score(data, center))
  
  if plot:
    plt.plot(centers, scores, linestyle='--', marker='o', color='b')
    plt.xlabel('K')
    plt.ylabel('Davies Bouldin score')
    plt.title('Davies Bouldin score vs. K')
    plt.show()
  return centers[np.argmin(scores)]

data = organize_data(df)

if __name__ == "__main__":
  max_c = 20
  dim = 6

  data_r = reduce(data, dim)

  score_g, df = GapStat(data_r, nrefs=5, maxClusters=max_c)
  print(score_g)
  ste = standard_error(df['gap'])
  s_prime = []
  for i in range(max_c-1):
    if i == 0:
      s_prime.append(ste)
    else:
      s_prime.append(s_prime[i-1]* ((21/20)**(1/2))) 



  plt.plot(df['clusterCount'], df['gap'], linestyle='--', marker='o', color='b')
  plt.errorbar(df['clusterCount'], df['gap'], yerr=s_prime)
  plt.xlabel('K')
  plt.ylabel('Gap Statistic')
  plt.title(f'Gap Statistic vs. K {dim} dimensions')
  plt.show()


