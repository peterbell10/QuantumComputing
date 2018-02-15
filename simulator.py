import circuit as ci
import scipy.sparse as sp
import numpy as np

def apply_gate(gate, register):
    if gate.gate_type = basis_gates.hadamard:
        return apply_hadamard(gate, quantum_register)
    elif gate.gate_type = basis_gates.contr_phase:
        return apply_c_phase(gate, quantum_register)


def apply_hadamard(gate, register):
    pass


def apply_square_matrix(mat, register, qbits):
    assert len(mat.shape) = 2          # Matrix
    assert mat.shape[0] = mat.shape[1] # Square
    size = len(register)
    w = np.zeros(size)
    for i in range(0, size):
        r = gather(i)
        i0 = i & ~scatter(r)
        for c in range(0, mat.shape[0]):
            j = i0 | scatter(c)
            w[i] = w[i] + mat[r, c] * register[j]
    return w

def gather(i, qbits):
    j = 0
    for k, qb_pos in enumerate(qbits):
        j = j | (((i >> qb_pos) & 1) << k)
    return j

def scatter(j):
    i = 0
    for k, qb_pos in enumerate(qbits):
        i = i | (((j << k) & 1) << qb_pos)
    return i
    
