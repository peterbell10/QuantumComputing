
class basis_gates:
    hadamard = 0  # Hadamard
    contr_phase = 1  # Controlled-phase gate

    @staticmethod
    def to_string(gate):
        return {
            basis_gates.hadamard:"Hadamard",
            basis_gates.contr_phase:"Controlled-phase"
        }[gate]

class gate:
    def __init__(self, gate_type):
        self.gate_type = int(gate_type)

    def operand_qbits(self):
        """Returns a list of all qbits this gate operates on"""
        raise NotImplementedError()

class hadamard_gate(gate):
    def __init__(self, qbit):
        gate.__init__(self, basis_gates.hadamard)
        self.qbit = int(qbit)

    def __str__(self):
        return 'Hadamard({})'.format(self.qbit)

    def operand_qbits(self):
        return [self.qbit]

class controlled_phase_gate(gate):
    def __init__(self, control_qbit, phase_qbit, phase):
        """Represents a binary controlled phase gate
        :param control_qbit index of the qbit determining whether the phase shift occurs
        :param phase_qbit index of the qbit to apply the phase change to
        :param phase phase change to apply **in turns**. i.e. 1 turn is a phase change of 2:math`\pi`
        """
        gate.__init__(self, basis_gates.contr_phase)
        self.control_qbit = control_qbit
        self.phase_qbit = phase_qbit
        self.phase = phase

    def __str__(self):
        return 'Controlled-phase({}, {})({} Turns)'.format(
        self.control_qbit, self.phase_qbit, self.phase)

    def operand_qbits(self):
        return [self.control_qbit, self.phase_qbit]

class circuit:
    def __init__(self):
        self.gates = []

    def __or__(self, other):
        """Concatenate another circuit onto this"""
        self.gates = self.gates + other.gates
        return self

    def __mul__(self, repeat_times):
        """Repeat this circuit multiple times"""
        self.gates = self.gates * repeat_times
        return self

    def __str__(self):
        return ' |\n'.join(str(g) for g in self.gates)

    def _add_gate(self, gate):
        """Add a single gate to the end of the circuit"""
        self.gates.append(gate)
        return self

def hadamard(qbit):
    return circuit()._add_gate(hadamard_gate(qbit))

def c_phase(control_qbit, phase_qbit, phase):
    return circuit()._add_gate(controlled_phase_gate(control_qbit, phase_qbit, phase))

def c_not(control_qbit, not_qbit):
    return (
        hadamard(not_qbit) |
        c_phase(control_qbit, not_qbit, 0.5) |
        hadamard(not_qbit))

def toffoli(control_1_qbit, control_2_qbit, not_qbit):
    return (
        hadamard(not_qbit) |
        c_phase(control_2_qbit, not_qbit, 0.25) |
        c_not(control_1_qbit, control_2_qbit) |
        c_phase(control_2_qbit, not_qbit, -0.25) |
        c_not(control_1_qbit, control_2_qbit) |
        c_phase(control_1_qbit, not_qbit, 0.25) |
        hadamard(not_qbit))

def adder(x_qbit, y_qbit, carry_qbit):
    return (
        toffoli(x_qbit, y_qbit, carry_qbit) |
        c_not(x_qbit, y_qbit))

if __name__ == '__main__':
    print(str(adder(1, 2, 3)))
