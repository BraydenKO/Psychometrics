from reader import df
from labels import factors
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np

width = 5
x_values = range(width,51,width)


def frequency(df,gender,factor):

  y_values = [0 for i in range(len(x_values))]

  columns = factors[factor]
  df = df.iloc[:,columns[0]:columns[1]][df["gender"] == gender]
  for i in range(len(df)):
    score = sum(df.iloc[i])
    for idx, val in enumerate(x_values):
      if score <= val:
        y_values[idx] += 1
        break

  return y_values

def fit(x, y):
  area = sum([i*width for i in y])

  data = []
  for i in range(len(x)):
    data.extend([x[i] for j in range(y[i])])

  mean, std = norm.fit(data)

  print(mean, std)

  q = np.linspace(width, 50, 100)
  p = norm.pdf(q, mean, std) * area
  return q, p, mean

def run(factor):
  factor = factor.title()

  women = frequency(df,2,factor)
  plt.plot(x_values, women, 'k-')
  q, p, m = fit(x_values, women)
  plt.plot(q, p, "g", linewidth = "3", alpha = 0.5)
  plt.axvline(x = m, ymax = max(p)/plt.ylim()[1], color = "g", alpha = 0.1)

  men = frequency(df,1,factor)
  plt.plot(x_values, men, 'b-')
  q, p, m = fit(x_values, men)
  plt.plot(q, p, "r", linewidth = "3", alpha = 0.5)
  plt.axvline(x = m, ymax = max(p)/plt.ylim()[1], color = "r", alpha = 0.1)

  plt.title(factor)
  plt.xlabel("frequency channels")
  plt.ylabel("amount of respondants")
  plt.show()

for factor in factors:
  run(factor)