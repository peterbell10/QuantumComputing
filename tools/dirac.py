import numpy as np

def ket(bitstring):
    ket = np.zeros((2**len(bitstring),1))
    ket[int(bitstring, 2)] = 1
    return(ket)

def bra(bitstring):
    bra = np.zeros((1, 2**len(bitstring)))
    bra[0][int(bitstring, 2)] = 1
    return(bra)

def tensor(a, b):
    space = np.kron(a, b)
    return space

