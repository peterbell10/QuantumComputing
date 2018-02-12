'''
Creates a quantum register of :math:`n` qubits.
'''

import numpy as np


class Quantum_Register(object):
    r"""
    Creates a quantum register of :math:`n` qubits. Initialises the state to :math:`|0\rangle`

    Args:
        no_of_qubits (int): The number of qubits, :math:`n`, necessary to represent the search space of size 
            :math:`2^n = N`.
    """
    def __init__(self, no_of_qubits):
        self.n_qubits = no_of_qubits
        self.states = 2**no_of_qubits
        self.qubits = np.zeros(self.states, dtype=complex)
        self.qubits[0] = 1.

    def __str__(self):
        return "\n".join(["{:0>3b} -> {:.4f}".format(state, self.qubits[state]) for state in range(self.states)])

    def measure(self):
        r"""
        Measures the result by calculating the probabilities of each quantum state.

        Returns:
            The determined solution.
        """
        probabilities = np.abs(self.qubits)**2
        return np.random.choice(len(probabilities), p=probabilities.flatten())

    def hadamard_matrix(self):
        r"""
        Generates a Hadamard matrix. The size of matrix will correspond to the number of qubits. For example,
        a register with a single qubit will return the following matrix

        .. math::
            H_1 = \frac{1}{\sqrt{2}}\begin{pmatrix}
            1 & 1\\ 
            1 & -1
            \end{pmatrix}.

        To get :math:`H_n`, the Hadamard matrix for a register with n qubits, the Kronecker product of :math:`H_1` and 
        :math:`H_{n-1}` is calculated. So for a register with 2 qubits,

        .. math::
            H_2 &= \text{kron}(H_1, H_1) \\
            H_2 &= \frac{1}{2}\begin{pmatrix}
                  1 & 1 & 1 & 1\\ 
                  1 & -1 & 1 & -1\\ 
                  1 & 1 & -1 & -1\\ 
                  1 & -1 & -1 & 1
                  \end{pmatrix}.

        Returns:
            The Hadamard matrix.
        """
        H = 1./np.sqrt(2.)*np.array([[1., 1.], [1., -1.]])
        matrix = np.array([1])

        for q in [1]*self.n_qubits:
            matrix = np.kron(H, matrix)
        return matrix
    
    def hadamard(self):
        """
        Aplies the Hadamard gate to the register.
        """
        self.qubits = self.hadamard_matrix().dot(self.qubits)
        return self


if __name__ == "__main__":
    register = Quantum_Register(4)
    had = register.hadamard_matrix()
    print(had.shape)
    # register.__str__()
    # print(register)
    # register.hadamard()
    # print(H_mat)


    