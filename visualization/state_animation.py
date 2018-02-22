import sys
sys.path.append("../")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from grover import *

fig = plt.figure(figsize=(10,4.5))
ax1 = fig.add_subplot(1,1,1)

grover_ = grover(4, 3)
states = grover_.ret_states()
x = np.arange(len(states[0]))
xlabels_ = []
for i in range(0, len(x)):
    xlabels_.append(r'\bf$|$' + str(x[i]) + r' $\rangle$')

def animate(i):
    ax1.clear()
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.title('Register State', fontsize = 16)
    plt.ylabel('State Amplitude', fontsize = 16)
    plt.ylim([-1,1])
    plt.xlim([-1, x[-1]+1])
    plt.xticks(x, xlabels_, fontsize=16)
    plt.plot((-10, x[-1]+10), (0,0), '-k')
    ax1.bar(x,states[i])

ani = animation.FuncAnimation(fig, animate, interval=1000, frames =len(states))
plt.show()
