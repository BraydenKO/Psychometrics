import matplotlib.pyplot as plt
from reader import df
from collections import Counter
from labels import factors, titles
import numpy as np
'''
Countries to look at:
US: United States (8,753)
GB: United Kingdom (1,531)
IN: India (1,464)
PH: Phillipines (649)
IT: Italy (277)
PK: Pakistan (222)
DE: Germany (191)
MY: Malaysia
'''
countries = ["US", "GB", "IN", "PH", "IT", "PK", "DE", "MY"]

def top_countries(df):
  c = Counter(df.loc[df["country"] != "(nu", "country"])
  top = c.most_common(10)
  print(top)

def country_avg(country):
  # Get only the users of that country
  users = df[df["country"] == country]

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
  for p in bars:
   height = round(p.get_height(), 3)
   ax[ax_idx].annotate('{}'.format(height),
      xy=(p.get_x() + p.get_width() / 2, height),
      xytext=(0, 3), # 3 points vertical offset
      textcoords="offset points",
      ha='center', va='bottom')

# 8 plots for the 8 countries
fig, ax = plt.subplots(8)

x_labels = titles.values()
colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "gray"]

all_scores = np.array([country_avg(country) for country in countries])
# Max value in each factor
max_val = all_scores.max(axis=0, keepdims=True)[0]
# Min value in each factor
min_val = all_scores.min(axis=0, keepdims=True)[0]
diff = list(max_val - min_val)
print({list(x_labels)[i]: diff[i] for i in range(len(x_labels))})

# Label the country
for idx, country in enumerate(countries):
  scores = all_scores[idx]
  pps = ax[idx].bar(x_labels, scores, color = colors[idx])
  ax[idx].set_xlabel(country)
  autolabel(pps, idx)

plt.subplots_adjust(hspace = 1, top = 0.95, bottom = 0.05)
plt.show()