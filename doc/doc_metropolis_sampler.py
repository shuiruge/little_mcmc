# Import module
import sys
sys.path.append('../sample/')
from metropolis_sampler import metropolis_sampler
import numpy as np
from random import uniform
from math import exp


# Preparing for metropolis_sampler
def target_distribution(x):
    return (  exp(- sum([c ** 2 for c in x]) / 100)
            + exp(- sum([c ** 2 for c in x]) / 30) * 20
            )

sigma = 1

init_vector = [uniform(-1, 1) for i in range(1)]


# Do sampling
chain = metropolis_sampler(target_distribution, sigma, init_vector, iterations=10000)


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
    
    plt.plot(plot_x, plot_y)
    plt.plot(plot_x, plot_target)
    plt.show()

plot_normalized(target_distribution, chain, num_bins=20)
# Return: accepted ratio = 0.9157,
# and a figure. So far so good.