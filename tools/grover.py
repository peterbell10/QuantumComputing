import os
from dirac import *
from qutip import snot
os.system('clear')

bits = 4

# create |0>
ket0 = ket('0')

# |0> ** (tensor * number of bits) -> ex: |000> for n=3
register = tensor_self(ket0, bits)
print('-register-\n', register, '\n')

# H ** (tensor * number of bits)
hada_full = hadamard(bits)
#hada_full = snot(bits).data.toarray()
#print('\n-hada_full-\n', hada_full)


# full superposition of the register ex: H**(tensor-3) on |000>
register = np.matmul(hada_full, register)
print('\n-register post-\n', register, '\n')

oracle = oracle('0001')
#print('\n-oracle-\n', oracle)

_diffuse = diffuse(register)
#print('\n-diffuse-\n', _diffuse)

register = np.matmul(oracle, register)
register = np.matmul(_diffuse, register)

print(register)


'''
TODO
1. apply oracle
2. apply diffuce
3. iterate 1,2
3. measure
'''
