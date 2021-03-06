#!/usr/bin/python
#
# Two identical Josephson junctions coupled via a quasiparticle current.
#
import math
import numpy
import sde
import sympy
import sys

def init_vector(sdei, i):
    return numpy.random.uniform(0.0, 2.0 * numpy.pi, sdei.num_threads)

# Random initial phase of the AC drive.
const_pars = {
        'phi0': lambda sdei: numpy.random.uniform(0.0, 2.0 * numpy.pi, sdei.num_threads)
    }

sim_params = {'i1': 'constant force on the 1st particle',
              'i2': 'constant force on the 2nd particle',
              'alpha': 'coupling strength',
              'd0': 'noise strength',
              'a1': 'AC drive amplitude for the 1st particle',
              'a2': 'AC drive amplitude for the 2nd particle',
              'omega': 'AC drive frequency'}

local_vars = {
        'ns0': lambda sdei: sympy.sqrt(sdei.S.d0 * sdei.S.dt),
        }

code = """
    dx0 = i1 - sinf(x0) + alpha * (i2 - sinf(x1)) + (a1 + alpha * a2) * cosf(omega * t + phi0);
    dx1 = i2 - sinf(x1) + alpha * (i1 - sinf(x0)) + (alpha * a1 + a2) * cosf(omega * t + phi0);
"""

ns_map = {0: ['ns0', 0], 1: [0, 'ns0']}
period_map = {0: sde.PeriodInfo(period=2.0 * math.pi, freq=1),
              1: sde.PeriodInfo(period=2.0 * math.pi, freq=1)}

sdei = sde.SDE(code, sim_params, num_vars=2, num_noises=2, const_pars=const_pars, noise_map=ns_map, period_map=period_map,
               local_vars=local_vars)

output = {'path': {
            'main': [sde.OutputDecl(func=sde.avg_moments, vars=[0, 1])],
            },
          'summary': {
            'main': [sde.OutputDecl(func=sde.drift_velocity, vars=[0, 1])],
#            'abs': [sde.OutputDecl(func=sde.abs_drift_velocity, vars=[0, 1])],
            }
        }

sdei.prepare(sde.SRK2, init_vector, freq_var='omega')
sdei.simulate(output)

