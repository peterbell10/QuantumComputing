import os
from dirac import *
import math
os.system('clear')

bits = 5
searchval = '00100'

# create |0>
ket0 = ket('0')

# |0> ** (tensor * number of bits) -> ex: |000> for n=3
register = tensor_self(ket0, bits)
print('-register-\n', register, '\n')

# H ** (tensor * number of bits)
hada_full = hadamard(bits)
#print('\n-hada_full-\n', hada_full)

# full superposition of the register ex: H**(tensor-3) on |000>
register = np.matmul(hada_full, register)
print('\n-register post-\n', register, '\n')

oracle = oracle(searchval)
#print('\n-oracle-\n', oracle)

_diffuse = diffuse(register)
#print('\n-diffuse-\n', _diffuse)

num_iters = (math.pi/4)*math.sqrt(2**bits)
if num_iters == 0:
    num_iters = 1
print('will iterate ', str(round(num_iters)), ' (', str(num_iters), ') times')

for i in range(0, round(num_iters)):
    register = np.matmul(oracle, register)
    register = np.matmul(_diffuse, register)
    print(register)


