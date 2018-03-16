import sys
sys.path.append("../")

from qutip import *
import matplotlib.pyplot as plt
import numpy as np
from circuit import circuit, hadamard, c_phase
from gates import cn_phase, c_not
from sim_py import sim_py

initial_state = 1 # 0 or 1
n_qbits = 1

i_state = basis(2, initial_state)
register = i_state

had = circuit()
had | hadamard(0)

sim = sim_py()
register = Qobj(sim.apply_circuit(had, register.full()))

b = Bloch()
b.add_states(i_state)
b.add_states(register)
b.show()
