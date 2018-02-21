import sys
sys.path.append("../")
import simulator
import circuit
import os
os.system('clear')
from dirac import *

bits = 3
searchval = '010'
ket0 = ket('0')
register = tensor_self(ket0, bits)

print(np.array([register]).T, '\n')

c = circuit.circuit()
for i in range(0, bits):
    c = c | circuit.hadamard(i)

register = simulator.apply_circuit(c, register)

print(np.array([register]).T, '\n')

grover = np.matmul(diffuse(np.array([register]).T), oracle(searchval))
grover = np.matmul(grover, grover)
register = np.matmul(grover, np.array([register]).T)

print(register)
