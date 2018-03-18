import numpy as np

from circuit import circuit, hadamard, c_phase
from gates import cn_phase, c_not
from sim_py import sim_py
import math
from fractions import gcd
import matplotlib.pyplot as plt

class quantum_period_finder:
    """Implements the quantum period finding part of Shor's algorithm."""
    def __init__(self, N, sim=sim_py()):
        """Initialise quantum registers for Shor's algorithm.

        :param int N: The number to be factorised
        """
        assert N > 1 # Cannot factorise that which has no factors

        # Word size is minimum bits required to represent N in binary
        self._word_qbits = int(math.ceil(math.log(N, 2)))
        # Need two sections of the same number of bits to hold f(x)
        self._n_qbits = 2 * self._word_qbits

        self._N = N
        self._register = np.zeros(2**(self._n_qbits), dtype=np.complex)
        self._register[0] = 1.0
        self._sim = sim

    def _QFT(self, inv=False):
        """Constructs the circuit for a quantum fourier transform (QFT).

        :param bool inv: If `True`, returns an inverse QFT (default `False`)
        :returns: QFT circuit
        :rtype: circuit.circuit
        """
        qft = circuit()
        for i in range(self._word_qbits):
            qft | hadamard(i)
            for j in range(self._word_qbits - i):
                if inv == False:
                    qft | c_phase((i + j + 1), i, (1/(1 << (1+j))))
                elif inv == True:
                    qft | c_phase((i + j + 1), i, (-1/(1 << (1+j))))
        return qft

    def _hadamard_low_word(self):
        had = circuit()
        for i in range(self._word_qbits):
            had | hadamard(i)
        return had

    def _prepare_register(self):
        self._register = self._sim.apply_circuit(self._hadamard_low_word(), self._register)

    def _low_mask(self):
        return (1 << self._word_qbits) - 1

    def _high_mask(self):
        return ((1 << self._n_qbits) - 1) & ~self._low_mask()

    def _get_low_word(self, i):
        return i & self._low_mask()

    def _set_low_word(self, i, x):
        return (i & self._high_mask()) | (x & self._low_mask())

    def _get_high_word(self, i):
        return (i & self._high_mask()) >> self._word_qbits

    def _set_high_word(self, i, x):
        return (i & self._low_mask()) | ((x << self._word_qbits) & self._high_mask())

    def _cheaty_f_map(self, a):
        new_reg = np.zeros_like(self._register)
        for i in range(len(self._register)):

            x = self._get_low_word(i)
            f_x = (a ** x) % self._N

            j = self._set_high_word(x, f_x)

            new_reg[j] += self._register[i]

        self._register = new_reg

    def estimate_inverse_period(self, a):

        self._prepare_register()

        # apply f-map
        self._cheaty_f_map(a)

        # apply the inverse QFT to the lower word in the register
        self._register = self._sim.apply_circuit(self._QFT(inv=True), self._register)

        # measure the register state and extract the estimate for the inverse period
        reg_meas = self._sim.measure(self._register)
        return self._get_low_word(reg_meas)

class shor:
    """Class implementing Shor's algorithm"""

    def __init__(self, N):
        # Prime factors need to exist
        assert N > 1
        self._N = N

    def choose_base(self):
        a = np.random.randint(low=2, high=self._N)
        while gcd(a, self._N) != 1:
            print("%s is a nontrivial factor" % gcd(a, self._N))
            a = np.random.randint(low=2, high=self._N)
        return a

    def check_prime(self):
        # TODO check if N is power of a prime
        if self._N <= 1:
            return False
        elif self._N <=3:
            return True
        elif self._N % 2 == 0 or self._N % 3 == 0:
            return False
        i = 5
        while i * i <= self._N:
            if self._N % i ==0 or self._N % (i+2) == 0:
                return False
            i += 6
        return True

    def denominator(self, x, qmax):
        r"""
        Finds the denominator :math:`q` of the rational number :math:`\frac{p}{q}` that best satisfies
        :math:`x \approx \frac{p}{q}` and :math:`q \lt q_max`
        """
        y = x
        q0 = q1 = q2 = 1
        qmax_sq = qmax * qmax

        while True:
            z = y - math.floor(y)
            if z < 0.5/qmax_sq:
                return q1
            y = 1 / z;
            q2 = math.floor(y) * q1 + q0
            if q2 >= qmax:
                return q1

            q0, q1 = q1, q2

    def run_shor(self):
        assert self.check_prime() == False, "number should not be a prime"

        while True:
            a = self.choose_base()
            print "N is %s and chosen (a) is %s with gcd of %s\n" % (self._N, a, gcd(a, self._N))


            # apply final classical number processing

            y = quantum_period_finder(self._N).estimate_inverse_period(a)
            Q = 2 ** math.ceil(math.log(self._N, 2))
            s = self.denominator(y, Q)

            print 'y = {}, Q = {}, s = {}'.format(y, Q, s)

            def _():
                n = 1
                s_n = s * n
                while s_n < Q:
                    if (a ** s_n) % self._N == 1:
                        # s_n is the period of the function
                        return s_n
                    n += 1
                    s_n = s * n

                # Can't find a solution, return an odd number so it'll be rejected
                return 1

            r = _()

            if r % 2 == 1:
                continue

            a_hr = a ** (r / 2)
            if a_hr % self._N == self._N - 1:
                continue

            print 'factor are: {}'.format([gcd(a_hr + 1, self._N), gcd(a_hr - 1, self._N)])
            break




if __name__ == '__main__':
    s = shor(77)
    s.run_shor()
