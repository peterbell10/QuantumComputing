"""Assorted composite gates"""

from circuit import hadamard, c_phase

def c_not(control_qbit, not_qbit):
    """Returns a controlled-not gate circuit"""
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
