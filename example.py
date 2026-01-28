import mplextras as plt2
import matplotlib.pyplot as plt
from numpy.random import rand

data = rand(10000)
plt2.hist(data, time=42, norm=True, errors=True, bins=50)
plt2.hist(data, time=21, norm=True, errors=True, bins=10)

plt.title("Histograms example with mpl-extras")
plt.xlabel("E (keV)")
plt.ylabel("Counts/keV/s")
plt.show()