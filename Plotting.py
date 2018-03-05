import matplotlib.pyplot as plt
import numpy as np

def first_hadamard_operation():

    x = np.arange(0, 8)
    y = np.zeros(len(x))
    # print(x, y)
    x_labels = [r"$|$"+'{:0>3b}'.format(0)+r"$\rangle $"]
    for state in x:
        label = r"$|$"+'{:0>3b}'.format(state)+r"$\rangle $"
        # print(label)
        x_labels.append(label)

    fig = plt.figure(figsize=(7,1))
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    ax = plt.gca()
    plt.scatter(x, y, s=0)
    plt.axhline(y=1/(2*np.sqrt(2)), color='k', linestyle='--')

    for state in x:
        # plt.axvline(x=state, color='k')
        plt.plot([state, state], [0, 1/(2*np.sqrt(2))], 'k', linewidth=1)

    plt.axis(xmax=7.3, xmin=-.3, ymax=1, ymin=0)
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticklabels(x_labels, fontsize=12)
    ax.xaxis.set_ticks_position('none') 
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    # ax.set_facecolor('red')
    plt.text(x=7.45, y=0.2, s=r'$\alpha_{\psi} = \frac{1}{2\sqrt{2}}$', fontsize=14)

    plt.subplots_adjust(bottom=0.27, right=0.8, left=0.15)
    # plt.savefig('Report/1st_hadamard_operation.png', facecolor='none')
    plt.savefig('Report/1st_hadamard_operation_transparent.png', transparent=True)

def oracle():

    x = np.arange(0, 8)
    y = np.zeros(len(x))
    # print(x, y)
    x_labels = [r"$|$"+'{:0>3b}'.format(0)+r"$\rangle $"]
    for state in x:
        label = r"$|$"+'{:0>3b}'.format(state)+r"$\rangle $"
        # print(label)
        x_labels.append(label)

    fig = plt.figure(figsize=(7,1))
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    ax = plt.gca()
    plt.scatter(x, y, s=0)
    plt.axhline(y=1/(2*np.sqrt(2)), color='k', linestyle='--')
    plt.axhline(y=0, color='k', linestyle='-')
    plt.axhline(y=-1/(2*np.sqrt(2)), color='k', linestyle='--')

    for state in x:
        if state != 5:
            plt.plot([state, state], [0, 1/(2*np.sqrt(2))], 'k', linewidth=1)
        else:
            plt.plot([state, state], [0, -1/(2*np.sqrt(2))], 'b', linewidth=1)
    plt.axis(xmax=7.3, xmin=-.3, ymax=0.5)
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticklabels(x_labels, fontsize=12)
    ax.xaxis.set_ticks_position('none') 
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['bottom'].set_color('white')
    # ax.set_facecolor('red')
    plt.text(x=7.45, y=0.2, s=r'$\alpha_{\psi} = \frac{1}{2\sqrt{2}}$', fontsize=14)
    plt.text(x=7.45, y=-0.55, s=r'$\alpha_{|101\rangle} = -\frac{1}{2\sqrt{2}}$', fontsize=14)

    plt.subplots_adjust(bottom=0.27, right=0.8, left=0.15)
    # plt.savefig('Report/1st_hadamard_operation.png', facecolor='none')
    plt.savefig('Report/oracle_transparent.png', transparent=True)

def diffusion():

    x = np.arange(0, 8)
    y = np.zeros(len(x))
    # print(x, y)
    x_labels = [r"$|$"+'{:0>3b}'.format(0)+r"$\rangle $"]
    for state in x:
        label = r"$|$"+'{:0>3b}'.format(state)+r"$\rangle $"
        # print(label)
        x_labels.append(label)

    fig = plt.figure(figsize=(7,1))
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    ax = plt.gca()
    plt.scatter(x, y, s=0)
    plt.axhline(y=1/(2*np.sqrt(2)), color='k', linestyle='--')
    plt.axhline(y=-1/(2*np.sqrt(2)), color='k', linestyle='--')

    for state in x:
        if state == 5:
            plt.plot([state, state], [0, 5/(4*np.sqrt(2))], 'b', linewidth=1)
        else:
            plt.plot([state, state], [0, 1/(4*np.sqrt(2))], 'k', linewidth=1)
    plt.axis(xmax=7.3, xmin=-.3, ymax=1, ymin=0)
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticklabels(x_labels, fontsize=12)
    ax.xaxis.set_ticks_position('none') 
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    # ax.set_facecolor('red')
    plt.text(x=7.45, y=0.2, s=r'$\alpha_{\psi} = \frac{1}{2\sqrt{2}}$', fontsize=14)
    plt.text(x=-1.8, y=-0.05, s=r'$\alpha_{|x\rangle} = \frac{1}{4\sqrt{2}}$', fontsize=14)
    plt.text(x=-2, y=0.7, s=r'$\alpha_{|101\rangle} = \frac{5}{4\sqrt{2}}$', fontsize=14)

    plt.subplots_adjust(bottom=0.27, right=0.8, left=0.15)
    plt.savefig('Report/diffusion_transparent.png', transparent=True)

def second_iteration():

    x = np.arange(0, 8)
    y = np.zeros(len(x))
    # print(x, y)
    x_labels = [r"$|$"+'{:0>3b}'.format(0)+r"$\rangle $"]
    for state in x:
        label = r"$|$"+'{:0>3b}'.format(state)+r"$\rangle $"
        # print(label)
        x_labels.append(label)

    fig = plt.figure(figsize=(7,1.5))
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    ax = plt.gca()
    plt.scatter(x, y, s=0)
    plt.axhline(y=1/(2*np.sqrt(2)), color='k', linestyle='--')
    plt.axhline(y=0, color='k', linestyle='-')
    plt.axhline(y=-1/(2*np.sqrt(2)), color='k', linestyle='--')

    for state in x:
        if state == 5:
            plt.plot([state, state], [0, 11/(8*np.sqrt(2))], 'b', linewidth=1)
        else:
            plt.plot([state, state], [0, -1/(8*np.sqrt(2))], 'k', linewidth=1)
    plt.axis(xmax=7.3, xmin=-.3, ymax=1.05)
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticklabels(x_labels, fontsize=12)
    ax.xaxis.set_ticks_position('none') 
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['bottom'].set_color('white')
    # ax.set_facecolor('red')
    plt.text(x=7.45, y=0.22, s=r'$\alpha_{\psi} = \frac{1}{2\sqrt{2}}$', fontsize=14)
    plt.text(x=-1.8, y=-0.3, s=r'$\alpha_{|x\rangle} = \frac{-1}{8\sqrt{2}}$', fontsize=14)
    plt.text(x=-2, y=0.8, s=r'$\alpha_{|101\rangle} = \frac{11}{8\sqrt{2}}$', fontsize=14)

    plt.subplots_adjust(bottom=0.175, right=0.8, left=0.15)
    # plt.savefig('Report/1st_hadamard_operation.png', facecolor='none')
    plt.savefig('Report/2nd_iteration_2_transparent.png', transparent=True)

# oracle()
# first_hadamard_operation()
# diffusion()
second_iteration()
# plt.show()