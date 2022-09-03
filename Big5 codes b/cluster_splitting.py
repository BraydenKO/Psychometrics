'''
Maps cluster with k = k1 to clusters with k = k2
'''
from cluster import df, organize_data, run_k_means, reduce, np

def cluster_mapping(data, k1, k2, dim):
  """Maps cluster with k = k1 to clusters with k = k2

  data: Dataset to work with (2d arry)
  k1: k for first set of clusters (int)
  k2: k for second set of clusters (int)
  dim: Number of dimensions to reduce data to (int)
  """
  data_r = reduce(data, dim)
  
  kmeans1 = run_k_means(data_r, k1, show = False)
  kmeans2 = run_k_means(data_r, k2, show=False)

  labels1 = kmeans1.labels_
  labels2 = kmeans2.labels_

  pairs =  np.column_stack((labels1, labels2))
  occurences = {}
  
  for cluster1, cluster2 in pairs:
    if cluster1 in occurences:
      if cluster2 in occurences[cluster1]:
        occurences[cluster1][cluster2] += 1
      else:
        occurences[cluster1][cluster2] = 1
    else:
      occurences[cluster1] = {cluster2:1}
  
  for cluster1, clusters in occurences.items():
    print(f"{cluster1} {clusters}")

  


if __name__ == "__main__":
  data = organize_data(df)
  
  cluster_mapping(data, 5, 16, 6)