from reader import df
from labels import factors
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
from statistics import median

# Creates the x values from 0 to 50
# with frequency channel width of {width} 
width = 5

# Gets the frequency for scores in each channel
# for a given gender and factor
def frequency(df,gender,factor):
  columns = factors[factor]
  x_values = range(width+(columns[1] - columns[0] + 1), width*(columns[1] - columns[0] + 1)+1, width)
  y_values = [0 for i in range(len(x_values))]

  # Gets the properly gendered users
  # And looks at the correct columns
  df = df.iloc[:,columns[0]:columns[1]][df["gender"] == gender]
  for col in df.columns:
    df = df[df[col].isin([1,2,3,4,5])]

  for i in range(len(df)):
    # for each user, get their summed score for this factor
    score = sum(df.iloc[i])
    # find which channel to put them in
    for idx, val in enumerate(x_values):
      if score <= val:
        y_values[idx] += 1
        break

  return y_values, x_values

# Fits the data to a normal distribution and return
# relevant data
def fit(x, y):

  data = []
  # turns the data received from frequency()
  # into a better format for calculation mean and std.
  # i.e. x = [5,10] and y = [1,3] -> data = [5,10,10,10]
  for i in range(len(x)):
    data.extend([x[i] for j in range(int(y[i]))])

  mean, std = norm.fit(data)

  print(f"mean: {mean}, std: {std}", end =" ")

  q = np.linspace(width, 50, 100)
  p = norm.pdf(q, mean, std)
  return q, p, mean, data, std

# For drawing some lines, one might want
# to find the vertical y value at the given x value
def get_height(x,y,i):
  try: # if it's a normal list
    index = x.index(i)
  except AttributeError: # if it's a numpy list and there aren't exact values
    for idx, j in enumerate(x):
      if j-i <= 0.5:
        index = idx
  return y[index]

# Runs everything normally
def run(factor):
  # makes sure the factor is first-letter capitalized
  factor = factor.title()

  # get the frequency data of women
  women, x_values = frequency(df,2,factor)
  # get the normal distribution (q,p), re-formatted data, and standard deviation
  q, p, m, data, std = fit(x_values, women)
  # plot the normal distribution
  plt.plot(q, p, "r", linewidth = "3", alpha = 0.5, label = "women")
  # plot the vertical line representing the mean
  plt.axvline(x = m, ymax = max(p)/plt.ylim()[1], color = "r", alpha = 0.5, label = f"women mean = {round(m,3)}")
  # adds the standard deviation to the legend
  plt.axvline(x = m+std, ymax = 0, color = "tab:pink", alpha = 0.5, label =f"women std={round(std,3)}")

  # scales down the collected data to be the same size as the fitted line
  # and the same size as the men (more women responded than men).
  area = sum([i*width for i in women])
  women = [i/area for i in women]

  # plot the collected data on women
  plt.plot(x_values, women, 'm', label = "women")
  med = median(data)
  # plot the vertical line representing the median (also will be the highest point on the collected data on women plot)
  plt.axvline(x = med, ymax = get_height(x_values,women,med)/plt.ylim()[1], color = "m", alpha = 0.1, label = f"women median = {int(med-width)}-{int(med)}")
  print(f"Skew: {3*(m-med)/std}")

  men, x_values = frequency(df,1,factor)
  q, p, m, data, std = fit(x_values, men)
  plt.plot(q, p, "b", linewidth = "3", alpha = 0.5, label = "men")
  plt.axvline(x = m, ymax = max(p)/plt.ylim()[1], color = "b", alpha = 0.5, label = f"men mean = {round(m,3)}")
  plt.axvline(x = m+std, ymax = 0, color = "c", alpha = 0.5, label =f"men std={round(std,3)}")

  area = sum([i*width for i in men])
  men = [i/area for i in men]

  plt.plot(x_values, men, 'g', label = "men")
  med = median(data)
  plt.axvline(x = med, ymax = get_height(x_values,men,med)/plt.ylim()[1], color = "g", alpha = 0.1, label = f"men median = {int(med-width)}-{int(med)}")
  print(f"Skew: {3*(m-med)/std}")

  # Tidying up the plot with titles, legend, and size
  plt.title(factor)
  plt.xlabel(f"frequency channels (width = {width})")
  plt.ylabel("amount of respondants")
  plt.legend(loc="upper left")
  plt.get_current_fig_manager().window.state('zoomed')
  plt.show()
  print("----------------------")

# Does the run function but without displaying the plots
# so that it can quickly calculate the standard deviations, means
# and give you the factor with the greatest difference in standard deviation
# (gender.py) will show the one with the greatest difference in mean

def run_std_diff():
  std_diff = []
  std_dict = {}

  def run_2(factor):
    factor = factor.title()

    women = frequency(df,2,factor)
    _, _, _, _, stdw = fit(x_values, women)

    area = sum([i*width for i in women])
    women = [i/area for i in women]

    men = frequency(df,1,factor)
    _, _, _, _, stdm = fit(x_values, men)
    std_diff.append(abs(stdw-stdm))
    std_dict[abs(stdw-stdm)] = factor
    print(f"{factor} : {abs(stdw-stdm)}")

    area = sum([i*width for i in men])
    men = [i/area for i in men]
  
  for factor in factors:
    run_2(factor)
  
  print(f"{std_dict[max(std_diff)]} : {max(std_diff)}")

for factor in factors:
 run(factor)

run("sensitivity")