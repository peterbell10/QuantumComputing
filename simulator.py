import circuit as ci
import scipy.sparse as sp
import numpy as np

def apply_gate(gate, register):
    if gate.gate_type == basis_gates.hadamard:
        return apply_hadamard(gate, quantum_register)
    elif gate.gate_type == basis_gates.contr_phase:
        return apply_c_phase(gate, quantum_register)


def apply_hadamard(gate, register):
    pass


def apply_square_matrix(mat, register, qbits):
    assert len(mat.shape) == 2          # Matrix
    assert mat.shape[0] == mat.shape[1] # Square
    size = len(register)
    w = np.zeros(size, dtype=np.complex)
    for i in range(size):
        r = gather(i, qbits) # i in the reduced basis
        i0 = i & ~scatter(r, qbits) # i but with all qbits in the reduced basis set to 0
        for c in range(mat.shape[0]): # iterate over matrix columns in reduced basis
            j = i0 | scatter(c, qbits) # translate from reduced basis to full basis using
                                       # the qbit values from i where it isn't in the
                                       # reduced basis
            w[i] += mat[r, c] * register[j] # Part of the matrix-vector multiply
    return w

def gather(i, qbits):
    """
    From an eigenstate of the computations basis (i) this constructs the
    corresponding eigenstate in the reduced basis consisting only of the
    state of the qbits in the given list.
    :param i an index into the quantum register
    :param qbits a list of the qbits to apply a square matrix to
    """
    j = 0
    for k, qb_pos in enumerate(qbits):
        a = ((i >> qb_pos) & 1) # eigenstate of the qbit at qb_pos
        j |= (a << k) # add the eigenstate to the tensor product of states
    return j

def scatter(j, qbits):
    """ The inverse of gather"""
    i = 0
    for k, qb_pos in enumerate(qbits):
        i |= (((j << k) & 1) << qb_pos)
    return i
