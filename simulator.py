import circuit as ci
import numpy as np
import cmath

def measure(register):
    """Measure the state of a quantum register

    :param numpy.array register: The state of the quantum register being measured
    :returns int: The measured eigenvalue
    """
    probabilities = np.abs(register)**2
    return np.random.choice(len(register), p=probabilities)

def apply_circuit(circuit, register):
    """Simulate the action of an entire circuit

    :param circuit.circuit circuit: The circuit to apply
    :param numpy.array register: The quantum register to apply the :class:`circuit` to
    :returns numpy.array: The new quantum register state
    """
    for gate in circuit.gates:
        register = apply_gate(gate, register)
    return register

def apply_gate(gate, register):
    """Simulate the action of a single basis gate

    :param circuit.gate gate: The gate to apply
    :param numpy.array register: The quantum register to apply the :class:`gate` to
    :returns numpy.array: The new quantum register state
    """
    if isinstance(gate, ci.hadamard_gate):
        hadamard_matrix = (1 / cmath.sqrt(2.+0.j)) * np.array([[1.+0.j , 1.+0.j],
                                                               [1.+0.j, -1.+0.j]])
        return apply_square_matrix(hadamard_matrix, register, gate.operand_qbits())
    elif isinstance(gate, ci.controlled_phase_gate):
        phase_matrix = np.eye(4, dtype=np.complex)
        phase_matrix[3, 3] = cmath.exp(2.j * cmath.pi * gate.phase)
        return apply_square_matrix(phase_matrix, register, gate.operand_qbits())

def apply_square_matrix(mat, register, qbits):
    """Simulate the action of a square matrix

    :param numpy.array mat: A square matrix with power of 2 dimensions :math:`\leq` the register
    :param numpy.array register: The quantum register to apply the matrix to
    :returns numpy.array: The new quantum register state
    """
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

    :param int i: an index into the quantum register
    :param list qbits: List of the qbits to apply a square matrix to
    """
    j = 0
    for k, qb_pos in enumerate(qbits):
        a = ((i >> qb_pos) & 1) # eigenstate of the qbit at qb_pos
        j |= (a << k) # add the eigenstate to the tensor product of states
    return j

def scatter(j, qbits):
    """The inverse of :func:`gather`

    :param int j: Eigenstate in the reduced basis
    :param list qbits: Index of the qbits that make up the reduced basis
    """
    i = 0
    for k, qb_pos in enumerate(qbits):
        i |= (((j >> k) & 1) << qb_pos)
    return i
