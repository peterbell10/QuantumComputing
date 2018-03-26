import numpy as np
import matplotlib.pyplot as plt

def plot_register(register, ax):
    num_eigenstates = len(register)
    x = np.arange(0, num_eigenstates)
    y = np.zeros_like(x)
    x_labels = [''] + [r'$|{:0>33}\rangle$'.format(i) for i in x]

    #figure.set_figheight(1)
    #figure.set_figwidth(num_eigenstates - 1)
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    #ax = plt.gca()

    for state, reg in zip(x, np.absolute(register)):
        ax.plot([state, state], [0, reg], 'k', linewidth=1)

    ax.set_yticks([])
    ax.set_yticklabels([])
    #ax.set_xticklabels(x_labels, fontsize=12)
    ax.xaxis.set_ticks_position('none')
    ax.spines['top'].set_color('white')
    #ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')

real_register = np.load('real_space.npy')
fourier_register = np.load('fourier_space.npy')

real_vals = np.zeros(0x100, dtype=np.complex)
fourier_vals = np.zeros(0x100, dtype=np.complex)

for i, x in enumerate(real_register):
    #real_vals[i & 0xFF] += x
    real_vals[(i >> 8) & 0xFF] += x

for i, x in enumerate(fourier_register):
    #fourier_vals[i & 0xFF] += x
    fourier_vals[(i >> 8) & 0xFF] += x

print np.argmax(fourier_vals)

_, (ax1, ax2) = plt.subplots(nrows = 2)
ax1.set_ylabel('State Amplitude')
ax2.set_ylabel('State Amplitude')
ax2.set_xlabel('State')
plot_register(real_vals, ax1)
plot_register(fourier_vals, ax2)
#plt.plot(np.absolute(real_vals))
#plt.plot(np.absolute(fourier_vals))
ax1.set_title('Befrore and After QFT')
plt.show()
