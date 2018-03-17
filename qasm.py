"""This module provides utilities for creating qasm output.
This is very useful because it allows creation of circuit diagram
graphics via the qasm2circ tool.
"""
from circuit import circuit, hadamard_gate, controlled_phase_gate
from itertools import chain

def _number_qbits(circ):
    """Returns the total number of qbits used in the given :class:`circuit.circuit`

    :param circuit.circuit circ: The circuit to inspect
    :returns: Number of qbits required to run the circuit `circ`
    :rtype: `int`
    """
    return 1 + max(chain.from_iterable(g.operand_qbits() for g in circ.gates))

def circuit_to_qasm(circ):
    """Returns a string of qasm code equivalent to the given :class:`circuit.circuit`

    :param circuit.circuit circ: The circuit to convert
    :returns: The circuit in qasm
    :rtype: `str`
    """

    # Define controlled-phase as a basic operation (Hadamard comes by default)
    qasm_str = "\tdef c-P,1,'\phi{}'\n"

    # Declare all the q(u)bits up front
    for i in range(_number_qbits(circ)):
        qasm_str += '\tqubit q{}\n'.format(i)

    # Output each gate in order as a qasm instruction
    for gate in circ.gates:
        if isinstance(gate, hadamard_gate):
            qasm_str += '\th\tq{}\n'.format(gate.qbit)
        elif isinstance(gate, controlled_phase_gate):
            qasm_str += '\tc-P\tq{},q{}\n'.format(gate.control_qbit, gate.phase_qbit)

    return qasm_str
