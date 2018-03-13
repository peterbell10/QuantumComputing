import numpy as np

from circuit import circuit, hadamard, c_phase
from gates import cn_phase, c_not
from sim_py import sim_py
import math
from fractions import gcd
import matplotlib.pyplot as plt


class shor:
    """Class implementing Shor's algorithm"""
    def __init__(self, n_qbits, N, sim=sim_py()):
        """Initialise shor's algorithm
        :param int n_qbits: The width of the quantum register
        """
        assert n_qbits > 1 # Wouldn't be much of a search, would it
        # Need an extra qbit that is always |1> to implement an unconditional not
        self._n_qbits = n_qbits
        self.m = n_qbits
        self.N = N
        self._register = np.zeros(2**(n_qbits + 1), dtype=np.complex)
        self._register_meas = np.zeros(2**(self.m + 1), dtype=np.complex)
        self._register[0] = 1.0
        self._register_meas[0] = 1.0
        self._sim = sim

    def check_prime(self, method="6kp1"):
        # TODO check if N is power of a prime
        if method == "6kp1":
            if self.N <= 1:
                return False
            elif self.N <=3:
                return True
            elif self.N % 2 == 0 or self.N % 3 == 0:
                return False
            i = 5
            while i * i <= self.N:
                if self.N % i ==0 or self.N % (i+2) == 0:
                    return False
                i += 6
            return True
        elif method == "miller-rabin":
            raise NotImplementedError()

    def classical(self):
        a = np.random.randint(low=2, high=self.N-1)
        while gcd(a, self.N) != 1:
            print("%s is a nontrivial factor" % gcd(a, self.N))
            a = np.random.randint(low=2, high=self.N)
        return a

    def QFT(self, inv=False):
        qft = circuit()
        for i in range(self._n_qbits):
            qft | hadamard(i)
            for j in range(self._n_qbits - i):
                if inv == False:
                    qft | c_phase((i + j + 1), i, (1/(1 << (1+j))))
                elif inv == True:
                    qft | c_phase((i + j + 1), i, (-1/(1 << (1+j))))
        return qft

    def hada_normal(self):
        had = circuit()
        for i in range(self._n_qbits):
            had | hadamard(i)
        return had

    def prepare_register(self):
        self._register = self._sim.apply_circuit(self.hada_normal(), self._register)

    def run_shor(self):
        assert self.check_prime() == False, "number should not be a prime"
        a = self.classical()
        print "N is %s and chosen (a) is %s with gcd of %s\n" % (self.N, a, gcd(a, self.N))

        # apply f-map

        # apply self.QFT(inv=True) to register

        # apply final classical number processing

    def measure(self):
        """Measure the current state"""
        return self._sim.measure(self.get_state())
