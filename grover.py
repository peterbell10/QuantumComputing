
import numpy as np

from circuit import circuit, hadamard
from gates import cn_phase, c_not
from sim_py import sim_py
import math


class grover:
    """Class implementing Grover's database search algorithm"""
    def __init__(self, n_qbits, target_state, sim=sim_py()):
        """Initialise grover's algorithm

        :param int n_qbits: The width of the quantum register
        :param int target_state: The value being searched for
        """
        assert n_qbits > 1 # Wouldn't be much of a search, would it
        # Need an extra qbit that is always |1> to implement an unconditional not
        self._n_qbits = n_qbits
        self._target_state = target_state
        self._iterate_op = self._grover_iterate()
        self._iterations = 0
        self._required_iterations = int(np.round(((math.pi / 4) * (2**(n_qbits / 2))), 0))
        self._register = np.zeros(2**(n_qbits + 1), dtype=np.complex)
        self._register[2**n_qbits] = 1.0
        self._register = sim.apply_circuit(self._hadamard_gate(), self._register)
        self._sim = sim

    def get_state(self):
        """Returns the current state of grover's algorithm"""
        # Highest qbit must be set
        assert (self._register[np.arange(2**self._n_qbits)] == 0).all()
        # Return state excluding the highest qbit
        return self._register[2**self._n_qbits : 2**(self._n_qbits + 1)]

    def _not_gate(self, not_qbit):
        """Returns an unconditional not gate"""
        # Highest qbit is always set to 1
        return c_not(self._n_qbits, not_qbit)

    def _conditional_phase_gate(self):
        """Returns a reflection in the :math:`|2^{n\\_qbits} - 1>` direction"""
        return cn_phase(range(1, self._n_qbits), 0, 0.5)

    def _hadamard_gate(self):
        """Returns a hadamard gate applied to each qbit of the register
        (excluding the highest bit used to implement `_not_gate`)
        """
        had = circuit()
        for i in range(self._n_qbits):
            had | hadamard(i)
        return had

    def _reflection(self, reflection_dir):
        """Returns a reflection across the given direction"""
        # Use unconditional not gates to change the condition under which
        # the conditional phase gate applies its phase change
        def nots():
            a = circuit()
            for i in range(self._n_qbits):
                if (reflection_dir & (1 << i)) == 0:
                    a | self._not_gate(i)
            return a
        return nots() | self._conditional_phase_gate() | nots()

    def _grover_iterate(self):
        """Returns a single iteration of grover's algorithm"""
        return (
            self._reflection(self._target_state) |
            self._hadamard_gate() |
            self._reflection(0) |
            self._hadamard_gate())

    def do_iteration(self):
        """Apply a single iteration of grover's algorithm to the internal state"""
        self._register = self._sim.apply_circuit(self._iterate_op, self._register)
        self._iterations += 1

    def execute(self):
        """Execute grover's algorithm until completion"""
        print self.get_state()
        while self._iterations < self._required_iterations:
            self.do_iteration()
            print self.get_state()

    def ret_states(self):
        """Return list of registers for every step of Grover's algorithm"""
        init_state = np.zeros(2**(self._n_qbits + 1), dtype=np.complex)
        init_state[2**self._n_qbits] = 1.0
        states = [init_state[2**self._n_qbits : 2**(self._n_qbits + 1)], self.get_state()]
        while self._iterations < self._required_iterations:
            self.do_iteration()
            states.append(self.get_state())
        return states

    def measure(self):
        """Measure the current state"""
        return self._sim.measure(self.get_state())

if __name__ == '__main__':
    g = grover(4, 6)
    g.execute()
    print 'Measured result: {}'.format(g.measure())
