import circuit as ci
import numpy as np
import cmath

class simulator:
    def measure(self, register):
        """Measure the state of a quantum register

        :param numpy.array register: The state of the quantum register being measured
        :returns int: The measured eigenvalue
        """
        probabilities = np.abs(register)**2
        return np.random.choice(len(register), p=probabilities)

    def apply_circuit(self, circuit, register):
        """Simulate the action of an entire circuit

        :param circuit.circuit circuit: The circuit to apply
        :param numpy.array register: The quantum register to apply the :class:`circuit` to
        :returns numpy.array: The new quantum register state
        """
        for gate in circuit.gates:
            register = apply_gate(gate, register)
        return register

    def apply_gate(self, gate, register):
        """Simulate the action of a single basis gate

        :param circuit.gate gate: The gate to apply
        :param numpy.array register: The quantum register to apply the :class:`gate` to
        :returns numpy.array: The new quantum register state
        """
        if isinstance(gate, ci.hadamard_gate):
            self.apply_hadamard(gate, register)
        elif isinstance(gate, ci.controlled_phase_gate):
            return self.apply_controlled_phase(gate, register)

    def apply_hadamard(self, gate, register):
        """Simulate the action of a single qbit hadamard gate

        :param circuit.hadamard_gate gate: The gate to apply
        :param numpy.array register: The quantum register to apply the :class:`hadamard_gate` to
        :returns numpy.array: The new quantum register state
        """
        raise NotImplementedError()

    def apply_controlled_phase(self, gate, register):
        """Simulate the action of a two qbit controlled-phase gate

        :param citcuit.controlled_phase_gate gate: The gate to apply
        :param numpy.array register: The quantum register to apply the :class:`controlled_phase_gate` to
        :returns numpy.array: The new quantum register state
        """
        raise NotImplementedError()
