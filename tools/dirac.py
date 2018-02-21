import numpy as np
import cmath
import math

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

def tensor_self(a, n=2):
    staticKet = np.array(a)
    space = np.array(a)
    for i in range(1, n):
        space = tensor(space, staticKet)
    return space

def hadamard(N=1):
    hadamard_matrix = (1 / math.sqrt(2.)) * np.array([[1. , 1.],
                                                      [1., -1.]])
    hadamard_matrix = tensor_self(hadamard_matrix, N)
    return hadamard_matrix

def oracle(bitstring):
    psi_k = ket(str(bitstring))
    psi_b = bra(str(bitstring))
    Rpsi = np.eye(2**len(bitstring)) - 2 * tensor(psi_k, psi_b)
    return Rpsi

def diffuse(register):
    wave_k = register
    wave_b = np.transpose(register)
    Rwave = - np.eye(len(register)) + 2 * tensor(wave_k, wave_b)
    return Rwave
