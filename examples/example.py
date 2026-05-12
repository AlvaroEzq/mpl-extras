import mplextras as plt2
import matplotlib.pyplot as plt
from numpy.random import rand

data = rand(10000)
plt2.hist(data, time=42, errors=True, bins=50, label="hist (t=42)")
plt2.hist(data, time=21, errors=True, bins=10, label="hist (t=21)")
plt2.sumhist([data, data], times=[42, 21], errors=True, bins=5, label="sumhist", color='forestgreen', fillalpha=0.25)
plt2.diffhist(data, data, time1=42, time2=21, errors=True, bins=5, label="diffhist", color='crimson', fillalpha=0.25)

plt.title("Histograms example with mpl-extras")
plt.xlabel("E (keV)")
plt.ylabel("Counts/keV/s")
plt.legend()
plt.show()