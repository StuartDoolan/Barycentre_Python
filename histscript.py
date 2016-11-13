from lincomtest import diff
import matplotlib.pyplot as plt
import numpy as np
plt.hist(diff, bins=np.logspace(-1, 1.0, 100))
plt.show()