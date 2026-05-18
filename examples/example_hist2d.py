import mplextras as plt2
import matplotlib.pyplot as plt
from numpy.random import normal

n_data = 10000
dataX = normal(0, 1, n_data)
dataY = normal(0, 1, n_data)
plt2.hist2d(dataX, dataY, time=42, bins=50, cbarinfo="meanboxerrorbar", cbarlabel="Counts / bin$^2$ / time", marginals=True, cmap="plasma")

plt.xlabel("X [mm]")
plt.ylabel("Y [mm]")
plt.show()