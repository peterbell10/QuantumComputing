import numpy as np

from circuit import circuit, hadamard, c_phase
from gates import cn_phase, c_not
from sim_nomat import sim_nomat
import math
from fractions import gcd
import matplotlib.pyplot as plt
import random

class quantum_period_finder:
    """Implements the quantum period finding part of Shor's algorithm."""
    def __init__(self, N, sim=sim_nomat()):
        """
        Initialise quantum registers for Shor's algorithm.

        :param int N: The number to be factorised
        """
        assert N > 1 # Cannot factorise that which has no factors

        # Word size is minimum bits required to represent N in binary
        self._word_qbits = int(math.ceil(math.log(N, 2)))
        # Need two sections of the same number of bits to hold f(x)
        self._n_qbits = 2 * self._word_qbits

        self._N = N
        self._sim = sim

    def _QFT(self, inv=False):
        """
        Constructs the circuit for a quantum fourier transform (QFT).

        :param bool inv: If `True`, returns an inverse QFT
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
        """
        Returns a hadamard gate that acts on all of the qbits in the low word.

        :returns: The hadamard circuit
        :rtype: :class:`circuit.circuit`
        """
        had = circuit()
        for i in range(self._word_qbits):
            had | hadamard(i)
        return had

    def _prepare_register(self):
        r"""
        Puts the register in the initial state for the period estimation routine.
        That is, the state

        .. math::

           |\psi{}\rangle = \frac{1}{\sqrt{2^q}}\sum_{i=0}^{2^q - 1} |i, 0\rangle

        where :math:`q` is the word size.
        """
        self._register = np.zeros(2**(self._n_qbits), dtype=np.complex)
        self._register[0] = 1.0
        self._register = self._sim.apply_circuit(self._hadamard_low_word(), self._register)

    def _low_mask(self):
        """
        Returns the bitmask for the low word of a cassical register/computational basis state.

        :returns: The mask
        :rtype: `int`
        """
        return (1 << self._word_qbits) - 1

    def _high_mask(self):
        """
        Returns the bitmask for the high word of a classical register/computational basis state.

        :returns: The mask
        :rtype: `int`
        """
        return ((1 << self._n_qbits) - 1) & ~self._low_mask()

    def _get_low_word(self, i):
        """
        :param int i: The two word register value to extract the low word from
        :returns: The low word of `i`
        :rtype: int
        """
        return i & self._low_mask()

    def _set_low_word(self, i, x):
        """
        :param int i: The two word register value to write the low word of
        :param int x: The new value to write to the low word of `i`
        :returns: `i` with the low word set to `x`
        :rtype: int
        """
        return (i & self._high_mask()) | (x & self._low_mask())

    def _get_high_word(self, i):
        """
        :param int i: The two word register value to extract the high word from
        :returns: The high word of `i`
        :rtype: int
        """
        return (i & self._high_mask()) >> self._word_qbits

    def _set_high_word(self, i, x):
        """
        :param int i: The two word register value to write the high word of
        :param int x: The new value to write to the high word of `i`
        :returns: `i` with the high word set to `x`
        :rtype: int
        """
        return (i & self._low_mask()) | ((x << self._word_qbits) & self._high_mask())

    def _modular_exponentiation(self, a):
        r"""
        Performs the modular exponentialtion of Shor's algorithm,
        performing the mapping

        .. math::

           |x, 0\rangle~\xrightarrow~|x, a^x \pmod{N}\rangle

        :param int a: The base for the exponentiation
        """
        new_reg = np.zeros_like(self._register)
        for i in range(len(self._register)):

            x = self._get_low_word(i)
            f_x = (a ** x) % self._N

            j = self._set_high_word(x, f_x)

            new_reg[j] += self._register[i]

        self._register = new_reg

    def estimate_frequency(self, a):
        """
        Uses quantum methods to find some integer multiple of the frequency of the
        modular exponentiation of a with high probability.

        :returns: The estimated frequency
        :rtype: `int`
        """

        self._prepare_register()

        # apply f-map
        self._modular_exponentiation(a)

        np.save('shor/real_space', self._register)

        # apply the inverse QFT to the lower word in the register
        self._register = self._sim.apply_circuit(self._QFT(), self._register)

        np.save('shor/fourier_space', self._register)

        # measure the register state and extract the estimate for the inverse period
        reg_meas = self._sim.measure(self._register)
        return self._get_low_word(reg_meas)


class shor:
    """Implements Shor's algorithm for integer factorisation"""

    def __init__(self, N):
        """
        Initialise Shor's algorithm with the number to be factorised(:math:`N`)

        :param int N: The number to be factorised
        """
        # Prime factors need to exist
        assert N > 2
        assert self._is_prime(N) == False, 'number should not be a prime'
        self._N = N

    def _choose_base(self):
        """
        Returns a random base to be used in Shor's algorithm.

        :returns: The base
        :rtype: `int`
        """
        assert self._N > 2
        return random.randrange(2, self._N)

    @staticmethod
    def _is_prime(x):
        """Returns `True` if x is prime"""
        if x <= 1:
            return False
        elif x <=3:
            return True
        elif x % 2 == 0 or x % 3 == 0:
            return False

        i = 5
        while i * i <= x:
            if x % i == 0 or x % (i+2) == 0:
                return False
            i += 6
        return True

    @staticmethod
    def _denominator(x, qmax):
        r"""
        Finds the denominator :math:`q` of the rational number :math:`\frac{p}{q}` that best satisfies

        .. math::

           x &\approx \frac{p}{q} \\
           q &\lt q_{max}
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
        """
        Evaluates Shor's factorisation algorithm with the number :math:`N` associated with the class.

        :returns: Two factors of :math:`N`
        :rtype: `list`
        """
        while True:
            base = self._choose_base()
            if (gcd(base, self._N) != 1):
                # If the base is a factor then we are done
                factor_a = gcd(base, self._N)
                return [factor_a, self._N / factor_a]

            print 'N is {} and exponent base (a) was chosen as {}'.format(self._N, base,)

            inv_period = quantum_period_finder(self._N).estimate_frequency(base)

            # Final classical number processing

            # Modulus for binary with just enough bits to fit N
            # Note floor(x) + 1 != ceil(x) when x is already an integer
            binary_modulus = 2 ** math.floor(math.log(self._N, 2)) + 1

            def find_exact_period():
                # The period should be some multiple of the denominator
                period_base = self._denominator(inv_period, binary_modulus)

                i = 1
                period_candidate = period_base * i
                while period_candidate < binary_modulus:
                    if (base ** period_candidate) % self._N == 1:
                        # Confirmed to be the true period
                        return period_candidate
                    i += 1
                    period_candidate = period_base * i

                # Can't find a solution, return an odd number so it'll be rejected later
                return 1

            period = find_exact_period()

            # period must be even for base^{r/2} to be a whole power of `base`
            if period % 2 == 1:
                continue


            # We know that x^2 = 1 (mod N), so (x - 1)(x + 1) = 0 (mod N)
            x = base ** (period / 2)

            # We know that x != 1 (mod N) because then r/2 would have been the period.
            # However, it might be that x == -1 (mod N), in which case the above equation
            # will include a multiplication by 0 (mod N) and not give a useful solution.
            if x % self._N == self._N - 1:  # i.e. -1 (mod N)
                continue

            # Return the factors of N
            return [gcd(x + 1, self._N), gcd(x - 1, self._N)]




if __name__ == '__main__':
    N = input('Enter a number to be factorised: ')
    if type(N) != int or N <= 0:
        print 'The number to factorise should be a positive integer'
    else:
        s = shor(N)
        factors = s.run_shor()
        print 'The factors were: {}'.format(factors)
