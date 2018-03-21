class gate:
    """Abstract base class for circuit basis gates"""
    def operand_qbits(self):
        """Returns a list of all qbits this gate operates on"""
        raise NotImplementedError()

class hadamard_gate(gate):
    """The single qbit hadamard gate"""
    def __init__(self, qbit):
        """
        Constructs a single qbit hadamard gate.

        :param int qbit: index of the qbit to apply the gate to
        """
        self.qbit = int(qbit)

    def __str__(self):
        return 'Hadamard({})'.format(self.qbit)

    def operand_qbits(self):
        return [self.qbit]

class controlled_phase_gate(gate):
    """The binary controlled-phase gate"""
    def __init__(self, control_qbit, phase_qbit, phase):
        """
        Constructs a two-qbit controlled-phase gate.

        :param int control_qbit: index of the qbit determining whether the phase shift occurs
        :param int phase_qbit: index of the qbit to apply the phase change to
        :param float phase: phase change to apply in *turns*. i.e. 1 turn is a phase change of :math:`2\pi`
        """
        self.control_qbit = control_qbit
        self.phase_qbit = phase_qbit
        self.phase = phase

    def __str__(self):
        return 'Controlled-phase({}, {})({} Turns)'.format(
        self.control_qbit, self.phase_qbit, self.phase)

    def operand_qbits(self):
        return [self.control_qbit, self.phase_qbit]

class circuit:
    """Class representing a quantum computation circuit."""
    def __init__(self):
        """Constructs an empty circuit"""
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
    """
    Returns a circuit of a single qbit hadamard gate.

    :param int qbit: The index of the qbit to apply the hadamard to.
    :returns: The hadamard circuit
    :rtype: circuit.circuit
    """
    return circuit()._add_gate(hadamard_gate(qbit))

def c_phase(control_qbit, phase_qbit, phase):
    """
    Returns a circuit of a two qbit controlled-phase gate.
    Note that `control_qbit` vs `phase_qbit` only really makes a difference
    when using the circuit to generate an image.

    :param int control_qbit: The index of the control qbit
    :param int phase_qbit: The index of the phase qbit
    :param float phase: The phase change to apply __in turns__. i.e. 1 turn is :math:`2 \times \pi`
    :returns: The controlled-phase circuit
    :rtype: circuit.circuit
    """
    return circuit()._add_gate(controlled_phase_gate(control_qbit, phase_qbit, phase))

if __name__ == '__main__':
    print(str(adder(1, 2, 3)))
