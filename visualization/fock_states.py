import sys
sys.path.append("../")

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from qutip import *
from grover import *



test = grover(3, 3)
states = test.ret_states()

x = np.arange(len(states[0]))
y = states[0]


plt.rc('text', usetex=True)
plt.rc('font', family='serif')


plt.bar(x, y)
xlabels_ = []
for i in range(0, len(y)):
    xlabels_.append(r'\bf$|$' + str(x[i]) + r' $\rangle$')
plt.title('Register State')
plt.xticks(x, xlabels_, fontsize=16)
plt.ylabel(r'\bf State Amplitude ', fontsize = 16)
plt.plot((-10, x[-1]+10), (0,0), '-k')
plt.ylim([-1,1])
plt.xlim([-1, x[-1]+1])
plt.show()

