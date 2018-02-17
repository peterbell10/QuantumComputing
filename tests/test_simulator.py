

import sys
sys.path.append("../")

import simulator
import circuit
import numpy as np
import numpy.testing
import numpy.linalg
import hypothesis as hyp
import hypothesis.strategies as strat
import hypothesis.extra.numpy
import cmath

@strat.composite
def register_and_qbits(draw, n_qbits, max_register_width):
    """Strategy to generate random quantum register and qbits to operate on"""
    register_width = draw(strat.integers(n_qbits, max_register_width))
    register = draw(hyp.extra.numpy.arrays(np.complex, 2**register_width))
    norm = np.linalg.norm(register)
    hyp.assume(np.isfinite(norm))
    hyp.assume(norm > 1e-7)
    register /= norm
    qbits = draw(strat.lists(
        strat.integers(0, register_width-1), min_size=n_qbits, max_size=n_qbits, unique=True))
    return (register, qbits)


def test_hadamard_zeros():
    """Test that hadamard appiled to the state |00> gives equal amplitudes to all states"""
    register = np.array([1.+0.j, 0.j, 0.j, .0j])
    c = circuit.hadamard(0) | circuit.hadamard(1)
    register = simulator.apply_circuit(c, register)
    np.testing.assert_allclose(
        register, 0.5*np.ones(4, dtype=np.complex), atol=1e-7)

@hyp.given(args=register_and_qbits(1, 6))
def test_hadamard_self_inverse(args):
    """Test that a hadamard applied twice is the identity"""
    register_init, qbits = args
    c = circuit.hadamard(qbits[0]) * 2
    register_final = simulator.apply_circuit(c, register_init)
    np.testing.assert_allclose(register_final, register_init, atol=1e-7)

@hyp.given(args = register_and_qbits(2, 6), phase = strat.floats(0.0, 1.0))
def test_cphase(args, phase):
    """Test that a cphase circuit is equivalent to the matrix version"""
    register, qbits = args
    cphase_circuit = circuit.c_phase(*qbits, phase=phase)
    cphase_matrix = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                              [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                              [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
                              [0.+0.j, 0.+0.j, 0.+0.j, cmath.exp(phase * 2.j * cmath.pi)]])
    assert_circuit_matrix_equivalent(cphase_circuit, cphase_matrix, qbits, register)

@hyp.given(args = register_and_qbits(2, 6), phase_1 = strat.floats(-1.0, 1.0), phase_2 = strat.floats(-1.0, 1.0))
def test_cphase_phases_add(args, phase_1, phase_2):
    """Test that two consecutive cphases are equivalent to a single cphase gate with the sum of the two phases"""
    register, qbits = args
    two_phase_circuit = (
        circuit.c_phase(*qbits, phase=phase_1) |
        circuit.c_phase(*qbits, phase=phase_2))
    sum_phase_circuit = circuit.c_phase(*qbits, phase=phase_1 + phase_2)
    assert_circuit_circuit_equivalent(two_phase_circuit, sum_phase_circuit, register)

def assert_close(a, b):
    """Compare equality with a tolerance to allow for rounding differences"""
    np.testing.assert_allclose(a, b, atol=1e-5)

def assert_circuit_matrix_equivalent(op_circuit, op_matrix, qbits, register):
    """Assert the circuit is equivalent to the matrix when applied to the given register"""
    assert_close(
        simulator.apply_circuit(op_circuit, register),
        simulator.apply_square_matrix(op_matrix, register, qbits))

def assert_circuit_circuit_equivalent(circuit_a, circuit_b, register):
    """Assert two circuits are equivalent when applied to the given register"""
    assert_close(
        simulator.apply_circuit(circuit_a, register),
        simulator.apply_circuit(circuit_b, register))
