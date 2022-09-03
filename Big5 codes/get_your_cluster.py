'''
Given a DataFrame with length 1 from r"data/your_response.csv",
find their cluster and graph it.
'''
from cluster import df, run_k_means, autolabel, question_avg, reduce, get_indeces, pd, plt, np, organize_data, norm_list
from fix_csv import fix_flips

def get_cluster_avg(k, dim, data,show=True,save=True):
  """Gets the averages for each question in a cluster and plot it and save it.

  k: Number of cluster (int)
  dim: Number of dimensions to reduce data to (int)
  data: 2d Array to work on (2d array)
  show: Whether the cluster bar graphs should be displayed (default True) (bool)
  save: Whether the averages data should be saved to r"data/cluster_results_Big5.csv"  (default True) (bool)
  """
  fig, ax = plt.subplots(k+2)
  fig.suptitle(f"PCA ({dim}), k={k}")

  data_r = reduce(data, dim)
  kmeans = run_k_means(data_r, k=k,dim=2, show=False)
  labels = kmeans.labels_
  indeces = get_indeces(labels)

  your_cluster = labels[-1]


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

  all_results.append(np.subtract(data[-1], global_averages))

  for idx, averages in enumerate(all_results):
    if k <= len(colors):
      pps = ax[idx].bar(x, averages, color = colors[idx])
    else:
      pps = ax[idx].bar(x, averages)
    if idx == len(all_results)-1:
      ax[idx].set_xlabel(f"You're in cluster {your_cluster+1}")
    else:
      ax[idx].set_xlabel(str(idx+1))
    autolabel(pps, ax, idx)

  pps = ax[k+1].bar(x, global_averages, color = colors[-1])
  ax[k+1].set_xlabel("total averages")
  autolabel(pps, ax, k+1)

  all_results.insert(0, ["Dim =", dim, "K =", k])
  all_results = pd.DataFrame(all_results)

  if save:
    all_results.to_csv(r"data/cluster_results_Big5b.csv", mode='a', sep = ",", index = False, header = False)

  if show:
    plt.subplots_adjust(hspace = 0.9)
    plt.show()

def get_response(data, columns):
  """Gets your response from r"data/your_response.csv" and preprocesses it.

  data: data to add your response to.
  columns: The columns of that dataset
  """
  from sklearn.preprocessing import MinMaxScaler
  path = (r"data/your_response.csv")
  response = pd.read_csv(path, sep=' ', header = None)
  response.columns = columns[:response.shape[1]]
  response = fix_flips(response, save = False, doprint=False)
  response = np.array(response)

  scaler = MinMaxScaler(feature_range=(0,1))
  response = scaler.fit_transform(response.reshape(-1,1)).reshape(1,-1)

  data = organize_data(data)
  data = np.append(data,response,axis=0)
  return data

if __name__ == "__main__":
  dim = 6
  k = 5
  data = get_response(df, df.columns)
  get_cluster_avg(k=k, dim=dim, data=data,show=True,save=False)
