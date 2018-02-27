import numpy as np
import cmath, math

import circuit as ci
from simulator import simulator

class sim_nomat(simulator):
    """Simulator implemented without any matrices"""

    @staticmethod
    def is_bit_set(i, bit):
        """Test whether a single bit of a number is set

        :param int i: Number to test
        :param int bit: The bit to test (0 indexed, little endian)
        :returns boolean: True if the bit is set
        """
        return ((i >> bit) & 1) != 0

    def apply_hadamard(self, gate, register):
        assert isinstance(gate, ci.hadamard_gate)
        new_reg = np.zeros_like(register)
        for i in range(len(register)):
            i0 = i & ~(1 << gate.qbit)
            i1 = i | (1 << gate.qbit)

            if sim_nomat.is_bit_set(i, gate.qbit):
                new_reg[i] = (register[i0] - register[i1]) / math.sqrt(2)
            else:
                new_reg[i] = (register[i0] + register[i1]) / math.sqrt(2)
        return new_reg


    def apply_controlled_phase(self, gate, register):
        assert isinstance(gate, ci.controlled_phase_gate)
        new_reg = np.zeros_like(register)
        for i in range(len(register)):
            if sim_nomat.is_bit_set(i, gate.control_qbit) and \
               sim_nomat.is_bit_set(i, gate.phase_qbit):
                new_reg[i] = register[i] * cmath.exp(2.j * cmath.pi * gate.phase)
            else:
                new_reg[i] = register[i]
        return new_reg
