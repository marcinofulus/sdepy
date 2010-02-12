#ifndef __CU_RNG_H
#define __CU_RNG_H

#define PI 3.14159265358979f

/*
 * Return a uniformly distributed random number from the
 * [0;1] range.
 */

%if rng == 'xorshift32':
__device__ float rng_xorshift32(unsigned int *state)
{
	unsigned int x = *state;

	x = x ^ (x >> 13);
	x = x ^ (x << 17);
	x = x ^ (x >> 5);

	*state = x;

	return x * 2.328306e-10f;
//	return x / 4294967296.0f;
}
%endif

%if rng == 'kiss32':
__device__ float rng_kiss32(unsigned int *x, unsigned int *y,
		unsigned int *z, unsigned int *w)
{
	*x = 69069 * *x + 1234567;		// CONG
	*z = 36969 * (*z & 65535) + (*z >> 16);	// znew
	*w = 18000 * (*w & 65535) + (*w >> 16);	// wnew  & 6553?
	*y ^= (*y << 17);			// SHR3
	*y ^= (*y >> 13);
	*y ^= (*y << 5);

	return ((((*z << 16) + *w) ^ *x) + *y) * 2.328306e-10;	// (MWC ^ CONG) + SHR3
}
%endif

%if rng == 'kiss':
__device__ float rng_kiss(unsigned int *x, unsigned int *y,
		unsigned int *z, unsigned int *c)
{
	unsigned long long t;
	unsigned long long a = 698769069ULL;

	*x = 69069 * *x + 12345;
	*y ^= (*y << 13);
	*y ^= (*y >> 17);
	*y ^= (*y << 5);
	t = a * *z + *c;

	*c = (t >> 32);

	return *x + *y + t;
}
%endif

/*
 * Generate two normal variates given two uniform variates.
 */
__device__ void bm_trans(float& u1, float& u2)
{
	float r = sqrtf(-2.0f * logf(u1));
	float phi = 2.0f * PI * u2;
	u1 = r * cosf(phi);
	u2 = r * sinf(phi);
}

#endif /* __CU_RNG_H */
