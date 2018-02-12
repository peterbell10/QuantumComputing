import numpy as np
import sys
from register import Quantum_Register


class Grover_Register(Quantum_Register):
    """
    Creates a register to implement Grover's algorithm. This regesiter inherits the properties of :func:`register`.
    
    .. figure:: //Users/Sahl/Desktop/University/Year_5/Quantum_Computing_Project/Project_code/Images/Grover's_circuit.png
        :width: 100%
        :align: center

        Circuit diagram of Grover's algorithm.
    """

    def __init__(self, n_qubits):
        super().__init__(n_qubits)
        self.cycles = np.pi/4*np.sqrt(2**self.n_qubits)

    def conditional_phase_shift(self):
        r"""
        Applies the conditional phase shift operator. It inverts all states except the :math:`|0\rangle`
        state .
        """
        for state in range(1,self.states):
            self.qubits[state] = -self.qubits[state]
        return self

    def diffusion_transform(self):
        """
        Applies the diffustion transform.
        """
        return self.hadamard().conditional_phase_shift().hadamard()

    def oracle(self):
        """
        Applies the Oracle. It inverts the state that satisfies the required condition.
        """
        target_state = 6
        self.qubits[target_state] = -self.qubits[target_state]
        return self

    def grover_algorithm(self):
        """
        Uses the Grover algorithm to determine the solution.

        Returns:
            The solution.
        """
        register.hadamard()
        for cycle in range(int(self.cycles)):
            self.oracle().diffusion_transform()
        return self.measure()

if __name__ == "__main__":
    for i in range(100):
        register = Grover_Register(4)
        measured_state = register.grover_algorithm()
        # print(register)
        print('measured state:', measured_state)


