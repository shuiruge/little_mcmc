"""
Description
---------
1. Herein the test target distribution is double-peak.
"""

# Import module
import sys
sys.path.append('../')
from sample.metropolis_sampler import metropolis_sampler
import numpy as np
from random import uniform
from math import exp


# Preparing for metropolis_sampler
# Test distribution
def dot(x, y):
    assert len(x) == len(y)
    return sum([x[i] * y[i] for i in range(len(x))])

def N(x, sigma):
    return exp(-0.5 * dot(x, x) / (sigma ** 2))

# Double-peak-test-function
distance_between_peaks = 50

def target_distribution(x):
    x1 = [_ - distance_between_peaks for _ in x]
    return 2 * N(x1, 5) + N(x, 5)


sigma = 10

init_vector = [uniform(-1, 1) for i in range(1)]


# Do sampling
chain = metropolis_sampler(target_distribution, sigma, init_vector, iterations=100000)


# Plot the result
import matplotlib.pyplot as plt

def plot_normalized(target_distribution, chain, num_bins=20):
    """ where target_distribution is from $\mathbb{R}$ to $\mathbb{R}$.
    """
    # bining along x-axis
    x_list = [_[0][0] for _ in chain]
    x_list.sort()
    step_length = (x_list[-1] - x_list[0]) / num_bins           
    x_bins = np.arange(x_list[0], x_list[-1], step_length)
    
    # y-axis
    y = [0]
    for i in range(len(x_bins) - 1):
        l = [_ for _ in x_list if x_bins[i] < _ and x_bins[i + 1] > _]
        y.append(len(l))
    target = [target_distribution([_]) for _ in x_bins]
    
    # plot
    plot_x = x_bins
    plot_y = [_ / max(y) for _ in y] # normalize
    plot_target = [_ / max(target) for _ in target] # normalize
    
    plt.plot(plot_x, plot_y, '.', plot_x, plot_target, '-')
    plt.legend(['sampled', 'target'])
    plt.show()

plot_normalized(target_distribution, chain, num_bins=20)
# Return: accepted ratio = 0.49937,
# and a figure. So far so good.
