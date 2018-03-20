import sys
sys.path.append("../")

from qutip import *
import matplotlib.pyplot as plt
import numpy as np
from circuit import circuit, hadamard, c_phase
from gates import cn_phase, c_not
from sim_py import sim_py
import cmath

def apply_phase(phase, register):
    phase_matrix = np.eye(2, dtype=np.complex)
    phase_matrix[1, 1] = cmath.exp(1.j * phase)
    return np.matmul(phase_matrix, register)

def create_point(theta, psi):
    x = np.sin(theta) * np.cos(psi)
    y = np.sin(theta) * np.sin(psi)
    z = np.cos(theta)
    return np.array([x, y, z])

initial_state = 1 # 0 or 1
n_qbits = 1

i_state = basis(2, initial_state)
register = i_state

had = circuit()
had | hadamard(0)

sim = sim_py()
register0 = Qobj(sim.apply_circuit(had, register.full()))

rot_theta0 = cmath.pi/2
rot_theta1 = cmath.pi/2
rot_psi0 = cmath.pi
rot_psi1 = 0

register1 = create_point(rot_theta1, rot_psi1)

dots = np.linspace(rot_psi0, rot_psi1, 25)

b = Bloch()
b.add_states(i_state)
b.add_states(register0)
b.add_vectors(register1)
b.add_points(create_point([rot_theta0 for i in dots], dots))
b.show()
