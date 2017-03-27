"""
Description
---------
1. This is an application of Metropolis sampler on finding the global maximum
   of any given distribution. This method is called the MCMC version of
   simulated annealing.

2. Herein the test distribution is double-peak.


Problems
------
1. When dimension is high, we find:
     
     1. either `gibbs=True` and thus gain a higher accepted ratio, but quite
        easy to be trapped into the local maximum, since the Gibbs sampler
        shorten the jump in the Markov process so that it cannot jump into
        the region of the higher peak;
      
     2. or `gibbs=False` and thus gain a tiny (even vanishing!) accepted ratio
        so that it cannot even move and then to find the global maximum.
"""

import metropolis_sampler as ms
from typing import List
import numpy as np
from random import uniform
from time import time

# Typing-hints
Array = np.array(List[float])


# Test distribution
def N(x: Array, sigma: float) -> float:
    return np.exp(-0.5 * np.dot(x, x) / (sigma ** 2))
# Double-peak-test-function
distance_between_peaks = 30

def test(x: Array) -> float:
    x1 = np.array([_ - distance_between_peaks for _ in x])
    return 200 * N(x1, 5) + N(x, 3)


# Annealing
annealing_temperature = 0.01

def annealed_test(x: Array, T=annealing_temperature):
    return np.exp(-1/T) * test(x)


# Do MCMC
dim = 2
sigma = 30
gibbsQ = True

init_vector = np.array([uniform(-20, 20) for i in range(dim)])

t_1 = time()
chain = ms.metropolis_sampler(annealed_test, sigma, init_vector,
                              iterations=10 ** 5, burn_in=1000, gibbs=gibbsQ
                              )
t_2 = time()

print('MCMC time spent = {0} seconds'.format(t_2 - t_1))


# Get the argmax
values = np.array([_[1] for _ in chain])
p = np.argmax(values)
print('argmax = {0}'.format(chain[p][0]))
