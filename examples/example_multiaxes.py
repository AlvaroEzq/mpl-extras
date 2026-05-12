import mplextras as plt2
import matplotlib.pyplot as plt
from numpy.random import normal, seed
seed(0)


data1 = normal(-1, 1, 10000)
data2 = normal(1, 1, 5000)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.set_layout_engine("tight")

ax1.set_title("Regular matplotlib hist function")
ax1.hist(data1, bins=100, label="plt.hist(data1, bins=100)")
ax1.hist(data2, bins=25, label="plt.hist(data2, bins=25)")
ax1.set_xlabel("E (keV)")
ax1.set_ylabel("Counts")
ax1.legend()


plt.sca(ax2) # mpl-extras functions are not implemented as methods of the axes, so we need to set the current axes before calling them.
plt.title("mpl-extras hist function")
plt2.hist(data1, time=10, bins=100, label="mplextras.hist(data1, bins=100, time=10)")
plt2.hist(data2, time=5, bins=25, label=  "mplextras.hist(data2, bins=25 , time=5 )")
plt.xlabel("E (keV)")
plt.ylabel("Counts/keV/s")
plt.legend()
plt.show()