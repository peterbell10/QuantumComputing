
#define PYOPENCL_DEFINE_CDOUBLE  // Enable double precision complex numbers
#include <pyopencl-complex.h>

bool is_bit_set(const int number, const int bit)
{
	return (number & (1 << bit)) != 0;
}

__kernel void hadamard(
	const unsigned qbit, __global cdouble_t * in_reg,
	__global cdouble_t * out_reg, const unsigned count)
{
	const int i = get_global_id(0);
	if (i >= count)
	{
		return;
	}

	const unsigned i0 = i & ~(1 << qbit);
	const unsigned i1 = i | (1 << qbit);
	const cdouble_t temp;

	if (is_bit_set(i, qbit))
	{
		temp = cdouble_sub(in_reg[i0], in_reg[i1]);
	}
	else
	{
		temp = cdouble_add(in_reg[i0], in_reg[i1]);
	}

	out_reg[i] = cdouble_mulr(temp, rsqrt(2))
}

__kernel void cphase(
	const unsigned int control_qbit, const unsigned phase_qbit, const double phase
	__global cdouble_t * in_reg, __global cdouble_t * out_reg, const unsigned int count)
{
	const int i = get_global_id(0);
	if (i >= count)
	{
		return;
	}

	if (is_bit_set(control_qbit) && is_bit_set(phase_qbit))
	{
		out_reg[i] = cdouble_mul(in_reg[i], cdouble_new(0.0, phase));
	}
	else
	{
		out_reg[i] = in_reg[i];
	}
}