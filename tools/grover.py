import os
from dirac import *
#from qutip import *
os.system('clear')

bits = 3

# create |0>
ket0 = ket('0')

# |0> ** (tensor * number of bits) -> ex: |000> for n=3
register = tensor_self(ket0, bits)
print('-register-\n', register, '\n')

# H ** (tensor * number of bits)
hada_full = hadamard(bits)
print('\n-hada_full-\n', hada_full)

# full superposition of the register ex: H**(tensor-3) on |000>
register = np.matmul(hada_full, register)
print('\n-register post-\n', register, '\n')

'''
TODO
1. apply oracle
2. apply diffuse
3. iterate 1,2
3. measure
'''
