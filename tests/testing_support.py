"""A collection of useful 'strategies' for generating test data"""

import hypothesis as hp
import hypothesis.strategies as st
import hypothesis.extra.numpy
import numpy as np
import numpy.linalg

@st.composite
def complex(draw, z_min, z_max):
    real = draw(st.floats(z_min.real, z_max.imag))
    imag = draw(st.floats(z_min.imag, z_max.imag))
    return real + 1.j*imag

@st.composite
def register(draw, n_qbits):
    states = 2**n_qbits
    register = draw(hp.extra.numpy.arrays(
        np.complex, states, fill = complex(-1-1j, 1+1j)))
    norm = np.linalg.norm(register)
    hp.assume(np.isfinite(norm))
    hp.assume(norm > 1e-7)
    register /= norm
    return register

@st.composite
def square_matrix(draw, n_qbits):
    states = 2**n_qbits
    square_matrix = draw(hp.extra.numpy.arrays(
        np.complex, (states, states), fill=complex(-1-1j, 1+1j)))
    return square_matrix
