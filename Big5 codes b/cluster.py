'''
Use to see how the clusters compare by indivual questions (get_cluster_avg(...))
or by factor (by_factor(...)) or display a bar graph from saved values on clusters (plot_from_csv(...))
'''
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from reader import df, pd
from labels import factors

def run_k_means(data, k, show = True, dim = 2):
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
  data_r = pca.transform(data)
  return data_r 

def plot(data, dim,label):
  """
  plots clusters in 2 or 3 dimensions and colors
  them based on label
  
  data: Dataset to plot
  dim: Number of dimensions to display in (2 or 3) (int)"""

  assert dim == 2 or dim == 3, f"Can only display clusters in 2 or 3 dimensions. You asked for {dim} dimensions"

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

def question_avg(data,indeces):
  """
  For the given rows of data, get the average 
  for each column (question)
  
  data: Dataset (numpy array)
  indexes: Which rows to look at (array)
  
  returns:
  x: Length of averages, makes it easy to plot averages (array)
  averages: Average value for each column (array)
  """
  data_n = data[indeces]
  averages = np.mean(data_n, axis=0)
  x = range(len(averages))
  return x, averages

def get_indeces(labels):
  """
  From labels that are returned from kmeans.labels_
  return a 2d array such that each row refers to a 
  cluster and the elements in the row are the indeces of
  rows in that cluster
  """
  indeces = [[] for _ in set(labels)]
  for idx, label in enumerate(labels):
    indeces[label].append(idx)
  return indeces

def autolabel(bars,ax, ax_idx):
  """Labels each bar with their average value.
  
  bars: The bars graphed (plt.bar())
  ax: Axes objects (matplotlib) to work on
  ax_idx: Which ax to label (int)
  """
  for p in bars:
   height = round(p.get_height(), 3)
   ax[ax_idx].annotate('{}'.format(height),
      xy=(p.get_x() + p.get_width() / 2, height),
      xytext=(0, 3), # 3 points vertical offset
      textcoords="offset points",
      ha='center', va='bottom')

def norm_list(data):
  """
  Used to see the differences from mean more 
  greatly. This is in the commneted section of below 
  functions. Uncomment if you want to use it.

  data: Array of what you want to scale
  
  returns:
  scaled: Array of same length as data but with scaled elements
  """
  if abs(min(data)) > abs(max(data)):
    maximum = abs(min(data))
  else:
    maximum = abs(max(data))
  scaled = []
  for i in data:
    scaled.append(i / maximum)
  return scaled

def factor_avg(users):
  """
  For a given factor, get the average for the users
  in that factor.

  users: 2d array of users to get average of

  returns:
  averages: Array of averages for each factor
  """
  users = pd.DataFrame(users)
  averages = []
  factor_sum = 0
  count = 0
  for cols in factors.values():
    for col in range(cols[0]-7,cols[1]-6):
        avg = users.iloc[:,col].mean()
        factor_sum += avg
        count += 1
    averages.append(factor_sum/count)
    factor_sum = 0
    count = 0

  return averages

def get_cluster_avg(k, dim, data,show=True,save=True):
  """Gets the averages for each question in a cluster and plot it and save it.

  k: Number of cluster (int)
  dim: Number of dimensions to reduce data to (int)
  data: 2d Array to work on (2d array)
  show: Whether the cluster bar graphs should be displayed (default True) (bool)
  save: Whether the averages data should be saved to r"data/cluster_results_Big5b.csv"  (default True) (bool)
  """
  fig, ax = plt.subplots(k+1)
  fig.suptitle(f"PCA ({dim}), k={k}")

  data_r = reduce(data, dim)
  kmeans = run_k_means(data_r, k=k,dim=2, show=False)
  labels = kmeans.labels_
  indeces = get_indeces(labels)
  colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "gray"]

  x, global_averages = question_avg(data,range(len(data)))

  all_results = []
  for cluster in indeces:
    x, averages = question_avg(data, cluster)
    averages = np.subtract(averages, global_averages)
    all_results.append(averages)

  #for column in range(len(all_results[0])):
  #  old_vals = [cluster[column] for cluster in all_results]
  #  new_vals = norm_list(old_vals)
  #  for idx, cluster in enumerate(all_results):
  #    cluster[column] = new_vals[idx]

  for idx, averages in enumerate(all_results):
    if k <= len(colors):
      pps = ax[idx].bar(x, averages, color = colors[idx])
    else:
      pps = ax[idx].bar(x, averages)
    ax[idx].set_xlabel(str(idx+1))
    #autolabel(pps, ax, idx)

  all_results.insert(0, ["Dim =", dim, "K =", k])
  all_results = pd.DataFrame(all_results)

  if save:
    all_results.to_csv(r"data/cluster_results_Big5b.csv", mode='a', sep = ",", index = False, header = False)

  if show:
    plt.show()

def by_factor(k, dim,data, show=True,save=True):
  """Gets the averages for each factor in a cluster and plots and saves it.
  
  k: Number of cluster (int)
  dim: Number of dimensions to reduce data to (int)
  data: 2d Array to work on (2d array)
  show: Whether the cluster bar graphs should be displayed (default True) (bool)
  save: Whether the averages data should be saved to r"data/cluster_results_Big5b.csv"  (default True) (bool)
  """
  fig, ax = plt.subplots(k)
  fig.suptitle(f"PCA ({dim}), k={k}")

  data_r = reduce(data, dim)
  kmeans = run_k_means(data_r, k=k,dim=2, show=False)
  labels = kmeans.labels_
  indeces = get_indeces(labels)
  colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "gray"]

  global_avg = factor_avg(data)
  x = range(5)
  all_results = []
  for cluster in indeces:
    averages = factor_avg(data[cluster])
    averages = np.subtract(averages, global_avg)
    all_results.append(averages)

  #for column in range(len(all_results[0])):
  #  old_vals = [cluster[column] for cluster in all_results]
  #  new_vals = norm_list(old_vals)
  #  for idx, cluster in enumerate(all_results):
  #    cluster[column] = new_vals[idx]

  for idx, averages in enumerate(all_results):
    print(f"Cluster {idx}: ", end = "")
    for score in averages:
      if score > 0.1:
        print("+", end = " ")
      elif score < -0.1:
        print("-", end = " ")
      else:
        print("0", end = " ")
    print()

    if k <= len(colors):
      pps = ax[idx].bar(x, averages, color = colors[idx])
    else:
      pps = ax[idx].bar(x, averages)
    ax[idx].set_xlabel(str(idx+1))
    autolabel(pps, ax, idx)

  all_results.insert(0, ["Dim =", dim, "K =", k])
  all_results = pd.DataFrame(all_results)

  if save:
    all_results.to_csv(r"data/cluster_results_Big5b.csv", mode='a', sep = ",", index = False, header = False)

  if show:
    plt.show()

def plot_from_csv(path, sep = ','):
  """If data is saved in a csv, plot the data in a bar graph.

  path: Path to read csv from (raw string r"")
  sep: The seperator in the csv file (default ',') (str) 
  """
  data = pd.read_csv(path, sep=sep)
  column_count = data.shape[0]
  dim = data.columns[1]
  k = data.columns[3]

  fig, ax = plt.subplots(len(data))
  fig.suptitle(f"PCA ({dim}), k={k}")

  x = range(column_count)
  colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "gray"]
  for idx, row in data.iterrows():
    if column_count <= len(colors):
      pps = ax[idx].bar(x, row, color = colors[idx])
    else:
      pps = ax[idx].bar(x, row)
    autolabel(pps, ax, idx)
  
  plt.show()

if __name__ == "__main__":
  dim = 6
  k = 4

  data = organize_data(df)
  by_factor(data, k, dim)

