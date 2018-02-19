"""Assorted composite gates"""

from circuit import hadamard, c_phase

def c_not(control_qbit, not_qbit):
    """Returns a controlled-not gate circuit"""
    return (
        hadamard(not_qbit) |
        c_phase(control_qbit, not_qbit, 0.5) |
        hadamard(not_qbit))

def cn_phase(control_qbits, phase_qbit, phase):
    """Returns a phase gate with an arbitrary list of control qbits"""
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
    """Returns a not gate with an arbitrary list of control qbits"""
    return (
        hadamard(not_qbit) |
        cn_phase(control_qbits, not_qbit, 0.5) |
        hadamard(not_qbit))

def adder(x_qbit, y_qbit, carry_qbit):
    return (
        cn_not([x_qbit, y_qbit], carry_qbit) |
        c_not(x_qbit, y_qbit))
