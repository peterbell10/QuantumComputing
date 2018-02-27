import numpy as np
import cmath

import circuit as ci
from simulator import simulator
import pyopencl as cl

class sim_opencl(simulator):
    """Simulator implemented using plain python"""
    def __init__(self):
        self._context = cl.create_some_context()
        self._queue = cl.CommandQueue(self._context)
        source = file('sim_opencl.cl', 'r').read()
        program = cl.Program(self._context, source).build()
        self._hadamard_kern = program.hadamard
        self._cphase_kern = program.cphase

    def apply_hadamard(self, gate, register):
        d_in_reg = cl.Buffer(self._context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf = register)
        d_out_reg = cl.Buffer(self._context, cl.mem_flags.WRITE_ONLY, register.nbytes)
        self._hadamard_kern(self._queue, register.shape, gate.qbit, d_in_reg, d_out_reg, len(register))

        h_out_reg = np.zeros_like(register)
        cl.enqueue_copy(self._queue, h_out_reg, d_out_reg)
        return h_out_reg

    def apply_controlled_phase(self, gate, register):
        d_in_reg = cl.Buffer(self._context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf = register)
        d_out_reg = cl.Buffer(self._context, cl.mem_flags.WRITE_ONLY, register.nbytes)
        self._cphase_kern(self._queue, register.shape, gate.control_qbit, gate.qbit, d_in_reg, d_out_reg, len(register))

        h_out_reg = np.zeros_like(register)
        cl.enqueue_copy(self._queue, h_out_reg, d_out_reg)
        return h_out_reg