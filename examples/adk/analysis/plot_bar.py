import numpy as np
import matplotlib.pyplot as plt

data = [4.75E-9, 6.54E-10]

data = [float(i)/sum(data) for i in data]

print(data)

plt.bar(1, data[0], facecolor="tomato")
plt.bar(2, data[1], facecolor="dodgerblue")

plt.xlim(0,3)
plt.ylim(0,1)
plt.xticks([1, 2], labels=[])
plt.show()
