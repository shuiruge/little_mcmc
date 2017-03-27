"""
Description
---------
1. This is an application of Metropolis sampler on finding the global maximum
   of any given distribution. This method is called the MCMC version of
   simulated annealing.

2. Herein the test distribution is double-peak.
"""

import sys
sys.path.append('../')
import sample.metropolis_sampler as ms

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
    return 200 * N(x1, 5) + N(x, 5)


# Annealing
annealing_temperature = 10

def annealed_test(x: Array, T=annealing_temperature):
    return np.exp(-1/T) * test(x)


# Do MCMC
dim = 30
sigma = 1

init_vector = np.array([uniform(-20, 20) for i in range(dim)])

t_1 = time()
chain = ms.metropolis_sampler(annealed_test, sigma, init_vector,
                              iterations=10 ** 5, burn_in=1000
                              )
t_2 = time()

print('MCMC time spent = {0} seconds'.format(t_2 - t_1))


# Get the argmax
values = np.array([_[1] for _ in chain])
p = np.argmax(values)
print('argmax = {0}'.format(chain[p][0]))
