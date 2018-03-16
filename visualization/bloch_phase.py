import sys
sys.path.append("../")

from qutip import *
import matplotlib.pyplot as plt
import numpy as np
from circuit import circuit, hadamard 
from gates import cn_phase, c_not
from sim_py import sim_py
import cmath


def apply_phase(phase, register):
    phase_matrix = np.eye(2, dtype=np.complex)
    phase_matrix[1, 1] = cmath.exp(1.j * phase)
    print phase_matrix
    return np.matmul(phase_matrix, register)

def create_point(theta, psi):
    x = np.sin(theta) * np.cos(psi)
    y = np.sin(theta) * np.sin(psi)
    z = np.cos(theta)
    return [x, y, z]

rot_theta0 = cmath.pi/4
rot_theta1 = cmath.pi/4
rot_psi0 = 0
rot_psi1 = cmath.pi/2
i_state = Qobj(create_point(rot_theta0, rot_psi0))

register = i_state
register = Qobj(np.array([1/np.sqrt(2), 1/np.sqrt(2)]))

print register
register = Qobj(apply_phase(cmath.pi/2., register.full()))
print register

b = Bloch()
dots = np.linspace(rot0, rot1)
b.add_points(create_point([cmath.pi/4 for i in dots], dots))

b.add_states(i_state)
b.add_states(register)
b.show()
