from reader import df
from labels import factors, titles
import matplotlib.pyplot as plt

# hand_label = {1: "Right", 2: "Left"}

def hand_avg(hand):
    users = df[df["hand"] == hand]
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
colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "gray"]

right = hand_avg(1)
plt.subplot(3,1,1)
plt.bar(x_labels, right, color = "red")
plt.xlabel("factors")
plt.ylabel("avg score")
plt.title("Right's average score")

left = hand_avg(2)
plt.subplot(3,1,2)
plt.bar(x_labels, left, color = "blue")
plt.xlabel("factors")
plt.ylabel("avg score")
plt.title("Left's average score")

# Plots the difference between right and left
plt.subplot(3,1,3)
plt.bar(x_labels, [left[i] - right[i] for i in range(len(x_labels))], color = "green")
plt.xlabel("factors")
plt.ylabel("avg score")
plt.title("average score difference (L - R)")

plt.subplots_adjust(hspace = 0.5)

plt.show()