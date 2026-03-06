import mplextras as plt2
import matplotlib.pyplot as plt
from numpy.random import rand

data = rand(10000)
plt2.hist(data, time=42, norm=True, errors=True, bins=50, label="hist (t=42)")
plt2.hist(data, time=21, norm=True, errors=True, bins=10, label="hist (t=21)")
plt2.sumhist([data, data], times=[42, 21], norm=True, errors=True, bins=5, label="sumhist")

plt.title("Histograms example with mpl-extras")
plt.xlabel("E (keV)")
plt.ylabel("Counts/keV/s")
plt.legend()
plt.show()