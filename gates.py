"""Assorted composite gates, useful for building into larger circuits"""

from circuit import hadamard, c_phase

def c_not(control_qbit, not_qbit):
    """
    Constructs a controlled-not gate circuit

    :param int control_qbit: Index of the control qbit
    :param int not_qbit: Index of the bit to be NOT-ed if the control bit is set
    :returns: The controlled-not circuit
    :rtype: circuit.circuit
    """
    return (
        hadamard(not_qbit) |
        c_phase(control_qbit, not_qbit, 0.5) |
        hadamard(not_qbit))

def cn_phase(control_qbits, phase_qbit, phase):
    """
    Returns a phase gate with an arbitrary non-empty list of control qbits
    Note that it doesn't really matter what is a `control_qbit` and what is a `phase_qbit`.
    Either way, the phase shift only occurs to the eigenstates where all qbits are 1.

    :param list control_qbits: List of indices for the control qbits
    :param int phase_qbit: Index of the qbit for the phase gate
    :returns: the c^n-phase circuit
    :rtype: circuit.circuit
    """
    assert len(control_qbits) > 0
    if len(control_qbits) == 1:
        return c_phase(control_qbits[0], phase_qbit, phase)
    else:
        head = control_qbits[0]
        tail = control_qbits[1:]
        half_phase = phase / 2
        return (
            c_phase(head, phase_qbit, half_phase) |
            cn_not(tail, head) |
            c_phase(head, phase_qbit, -half_phase) |
            cn_not(tail, head) |
            cn_phase(tail, phase_qbit, half_phase))

def cn_not(control_qbits, not_qbit):
    """
    Returns a not gate with an arbitrary list of control qbits

    :param list control_qbits: List of indices for control qbits
    :param int not_qbit: The qbit to apply the NOT gate to
    :returns: The c^n-NOT gate circuit
    :rtype: circuit.circuit
    """
    return (
        hadamard(not_qbit) |
        cn_phase(control_qbits, not_qbit, 0.5) |
        hadamard(not_qbit))
