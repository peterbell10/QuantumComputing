"""Tests for simulator.apply_square_matrix"""

import sys
sys.path.append("../")

import hypothesis as hyp
import hypothesis.strategies as strat
import hypothesis.extra.numpy
import numpy as np
import numpy.testing
import numpy.linalg
import simulator
import math

import testing_support


def apply_square_matrix(mat, register, qbits):
    """Implementation given in lectures as a test oracle"""
    def gather(i, qbits):
        j = 0
        for k, qb_pos in enumerate(qbits):
            a = ((i >> qb_pos) & 1)
            j |= (a << k)
        return j

    def scatter(j, qbits):
        i = 0
        for k, qb_pos in enumerate(qbits):
            i |= (((j >> k) & 1) << qb_pos)
        return i

    size = len(register)
    w = np.zeros(size, dtype=np.complex)
    for i in range(size):
        r = gather(i, qbits)
        i0 = i & ~scatter(r, qbits)
        for c in range(mat.shape[0]):
            j = i0 | scatter(c, qbits)
            w[i] = w[i] + mat[r, c] * register[j]
    return w

@strat.composite
def apply_matrix_args_strategy(draw, sequential_qbits):
    """Generates a random quantum register and square matrix of dimension <= the register.
    As well as a list of qbits to apply the matrix to.
    """
    n_qbits = draw(strat.integers(2, 6))
    matrix_size = draw(strat.integers(1, min([4, n_qbits-1])))
    square_matrix = draw(testing_support.square_matrix(matrix_size))
    register = draw(testing_support.register(n_qbits))
    qbits = []
    if sequential_qbits:
        qbit_start = draw(strat.integers(0, n_qbits - matrix_size))
        qbits = list(range(qbit_start, qbit_start + matrix_size))
    else:
        qbits = draw(strat.lists(
            strat.integers(0, n_qbits - 1), min_size=matrix_size, max_size=matrix_size, unique=True))
    return (square_matrix, register, qbits)

@hyp.given(args=apply_matrix_args_strategy(False))
def test_matches_oracle(args):
    """Test that the simulator apply matches the implementation from lectures"""
    np.testing.assert_allclose(
        simulator.apply_square_matrix(*args),
        apply_square_matrix(*args),
        atol=1e-5
    )
