# 1 is male, 2 is female, 3 is other, 0 if missed
from reader import df, pd
from labels import factors, titles
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)

# For a given gender, go through all of the
# factors and return average in that factor.
# Refer to country.py for more comments since
# it has a similar structure.
def sex_avg(gender):
    users = df[df["gender"] == gender]
    averages = []
    factor_sum = 0
    count = 0

    for cols in factors.values():
        for col in range(cols[0],cols[1]+1):
            avg = users[users.iloc[:,col].isin([1,2,3,4,5])].iloc[:,col].mean()
            factor_sum += avg
            count += 1
        averages.append(factor_sum/count)
        factor_sum = 0
        count = 0

    return averages

x_labels = titles.values()

men = sex_avg(1)
plt.subplot(3,1,1)
plt.bar(x_labels, men, color = "red")
plt.xlabel("factors")
plt.ylabel("avg score")
plt.title("Men's average score")

women = sex_avg(2)
plt.subplot(3,1,2)
plt.bar(x_labels, women, color = "blue")
plt.xlabel("factors")
plt.ylabel("avg score")
plt.title("Women's average score")

# Plots the difference between men and women
plt.subplot(3,1,3)
plt.bar(x_labels, [women[i] - men[i] for i in range(len(x_labels))], color = "green")
plt.xlabel("factors")
plt.ylabel("avg score")
plt.title("average score difference (w - m)")

plt.subplots_adjust(hspace = 0.5)

plt.show()

