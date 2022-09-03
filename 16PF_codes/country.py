'''
Plots the average for each factors for the given countries
'''

from reader import df, pd
from labels import factors
import matplotlib.pyplot as plt
import numpy as np
'''
Countries to look at:
US: United States (23,988)
GB: United Kingdom (5,056)
IN: India (3,259)
CA: Canada (2,647)
AU: Australia (2,539)
PH: Phillipines (2,069)
SG: Singapore (466)
MY: Malaysia (405)
'''
countries = ["US", "GB", "IN", "CA", "AU", "PH", "SG", "MY"]

pd.set_option('display.max_rows', None)

def country_avg(country):
  """
  Given a country return a list of averages
  where each average is that country's average
  score in that factor.

  country: Which country to return the average of (str)

  returns:
  averages: An array where each element is that index's factor's average (array)
  """

  # Get only the users of that country
  users = df[df["country"] == country]

  averages = []

  # counts the average of each column
  factor_sum = 0

  # counts the number of columns 
  # for that factor
  count = 0

  # records which factor you're
  # in, which will be a letter
  # corresponding to a factor
  label = 0
 
  for col in df.columns:
        if col == "age": # Stoping point
            averages.append(factor_sum/count)
            break
        
        # If the current label isn't the old label
        # You're on a new set
        # Since you're on a new set, add the average score to 
        # {averages} a reset {factor_sum} and {count}
        if col[0] != label and label != 0:
            averages.append(factor_sum/count)
            factor_sum = 0
            count = 0

        label = col[0]
        count += 1

        avg = users[users[col].isin([1,2,3,4,5])][col].mean()
        factor_sum += avg

  return averages

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
  # 8 plots for the 8 countries
  fig, ax = plt.subplots(8)

  x_labels = factors.keys()
  colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "gray"]

  all_scores = np.array([country_avg(country) for country in countries])
  # Max value in each factor
  max_val = all_scores.max(axis=0, keepdims=True)[0]
  # Min value in each factor
  min_val = all_scores.min(axis=0, keepdims=True)[0]
  diff = list(max_val - min_val)
  print({list(x_labels)[i]: diff[i] for i in range(16)})

  # Label the country
  for idx, country in enumerate(countries):
    scores = all_scores[idx]
    pps = ax[idx].bar(x_labels, scores, color = colors[idx])
    ax[idx].set_xlabel(country)
    autolabel(pps, idx)


  plt.subplots_adjust(hspace = 1)
  plt.show()