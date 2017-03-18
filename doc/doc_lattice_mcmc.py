"""
We display an instance to show how to use the functions in the `lattice_mcmc.py`.

We are to get the argmax of function defined by
    
        f(x) := - sum( [__ ** 2 for __ in x] )
        
which has unique argmax `x[i] = 0` for all `i`.

We are to:
    
    1. get the result by function `lattice_mcmc.mcmc`;
    
    2. get the result by function `lattice_mcmc.single_chain_mcmc`, on which
       you can set `init_position` alternatively.
"""


# Import module
import sys
sys.path.append('../sample/')
import lattice_mcmc
from numpy import arange
from time import time

# Typing-hints
from typing import List, Callable, Tuple, Mapping, Any
Position = List[int]
Value = float
VariableRange = List[List[float]]


# Define test-function
def f(x: List[float]) -> Value:
    return - sum( [__ ** 2 for __ in x] )

# The variable-range is x[i] in range(0, 1, 0.1)
dim = 5
x_range = [arange(0, 1, 0.1) for i in range(dim)]


# ========= Do MCMC =========

# First make f on lattice.
def latticed_f(position: Position) -> Value:
    x = [x_range[i][position[i]] for i in range(len(position))]
    return f(x)

# Set parameter of lattice_mcmc
chain_num = 2
tolerence = 0.01
lattice_size = [len(x_range[i]) for i in range(dim)]

# Print the spent interval of time
t_begin = time()

mcmc_chains = lattice_mcmc.mcmc(chain_num, tolerence,
                                lattice_size, latticed_f
                                )

t_end = time()

print('time spent: ', t_end - t_begin)

# Print the end node of each chain
for i in range(chain_num):
    print('End node of chain ' + str(i) + ': ',
          mcmc_chains[i][-1]
          )
# Return
# time spent:  0.010267972946166992
# End node of chain 0:  ([0, 0, 0, 0, 0], -0.0)
# End node of chain 1:  ([0, 0, 0, 0, 0], -0.0)

# It's extremely fast forsooth!


# When employin `lattice_mcmc.mcmc`, the initial position is randomly sampled
# on the whole lattie. However, sometime we have to restrict the initial
# position by our needs, e.g. in training ANN. To do so, we can employ functions
# `lattice_mcmc.random_position` and `lattice_mcmc.random_position`, as follow.

# Restrict initial position s.t. it's close to the origin.
init_position = random_position([round(__ / 3) + 1 for __ in lattice_size])

mcmc_chain = lattice_mcmc.single_chain_mcmc(
                     tolerence, lattice_size,
                     latticed_f, init_position
                     )

print( 'End node of chain :', mcmc_chain[-1] )
# Return
# End node of chain : ([0, 0, 0, 0, 0], -0.0)