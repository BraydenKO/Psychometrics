'''
Plots a bar graph for men and women and their average in each factor
'''
from reader import df, pd
from labels import factors
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)

# For a given gender, go through all of the
# factors and return average in that factor.
# Refer to country.py for more comments since
# it has a similar structure.
def sex_avg(gender):
  """
  For a given gender, go through all of the factors
  and return the average in that factor.
  Similar to country.py, so go there for more in depth comments.
  
  gender: Men are 1 and women are 2 - that's how the data labels them (int)
  
  returns:
  averages: An array where each element is that index's factor's average (array)
  """
  users = df[df["gender"] == gender]
  averages = []
  factor_sum = 0
  count = 0
  label = 0

  for col in df.columns:
      if col == "age":
          averages.append(factor_sum/count)
          break

      if col[0] != label and label != 0:
          averages.append(factor_sum/count)
          factor_sum = 0
          count = 0

      label = col[0]
      count += 1

      avg = users[users[col].isin([1,2,3,4,5])][col].mean()
      factor_sum += avg

  return averages

if __name__ == "__main__":
  men = sex_avg(1)
  plt.subplot(3,1,1)
  plt.bar(factors.keys(), men, color = "red")
  plt.xlabel("factors")
  plt.ylabel("avg score")
  plt.title("Men's average score")

  women = sex_avg(2)
  plt.subplot(3,1,2)
  plt.bar(factors.keys(), women, color = "blue")
  plt.xlabel("factors")
  plt.ylabel("avg score")
  plt.title("Women's average score")

  # other = sex_avg(3)
  # plt.subplot(3,1,3)
  # plt.bar(factors.keys(), other, color = "yellow")
  # plt.xlabel("factors")
  # plt.ylabel("avg score")
  # plt.title("Other's average score")

  # Plots the difference between men and women
  plt.subplot(3,1,3)
  plt.bar(factors.keys(), [women[i] - men[i] for i in range(16)], color = "green")
  plt.xlabel("factors")
  plt.ylabel("avg score")
  plt.title("average score difference (w - m)")

  plt.subplots_adjust(hspace = 0.4)

  plt.show()

