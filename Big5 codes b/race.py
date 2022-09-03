from reader import df
from labels import race_label, factors, titles
import matplotlib.pyplot as plt
import numpy as np

'''
Races to look at:
Caucasian (European) (3) : 10,537
South East Asian (11) : 1,861
Indian (4) : 1,518
Middle East (5) : 515
'''
races = [3, 11, 4, 5]
def top_races(df):
  """Tool used to find which are the 10 most common races in df.

  df: pandas DataFrame

  returns:
  top: The 10 most common races and their count (array)
  """
  from collections import Counter
  c = Counter(df.loc[:,'race'])
  top = c.most_common(10)
  result = []
  for i in top:
    result.append((race_label[i[0]], i[0],i[1]))
  print(result)

def race_avg(race):
  # Get only the users of that country
  users = df[df["race"] == race]

  averages = []

  # counts the average of each column
  factor_sum = 0

  # counts the number of columns 
  # for that factor
  count = 0
 
  for cols in factors.values():
    for col in range(cols[0], cols[1]+1):
      avg = users[users.iloc[:,col].isin([1,2,3,4,5])].iloc[:,col].mean()
      
      factor_sum += avg
      count += 1
    
    averages.append(factor_sum/count)
    factor_sum = 0
    count = 0
  
  return averages

# Labels each bar with their average value
def autolabel(bars, ax_idx):
  """Labels each bar with their average value.
  
  bars: The bars graphed (plt.bar())
  ax_idx: Which ax to label (int)
  """
  for p in bars:
   height = round(p.get_height(), 3)
   ax[ax_idx].annotate('{}'.format(height),
      xy=(p.get_x() + p.get_width() / 2, height),
      xytext=(0, 3), # 3 points vertical offset
      textcoords="offset points",
      ha='center', va='bottom')

if __name__ == "__main__":
  fig, ax = plt.subplots(4)
  x_labels = titles.values()
  colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "gray"]

  all_scores = np.array([race_avg(country) for country in races])
  max_val = all_scores.max(axis=0, keepdims=True)[0]
  min_val = all_scores.min(axis=0, keepdims=True)[0]
  diff = list(max_val - min_val)
  print({list(x_labels)[i]: diff[i] for i in range(len(x_labels))})

  for idx, race in enumerate(races):
    scores = all_scores[idx]
    pps = ax[idx].bar(x_labels, scores, color = colors[idx])
    ax[idx].set_xlabel(race_label[race])
    autolabel(pps, idx)

  plt.subplots_adjust(hspace = 0.9)
  plt.show()
