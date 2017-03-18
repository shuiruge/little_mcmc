
import sys
sys.path.append('../sample/')
import lattice_mcmc
from numpy import arange
from time import time

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

# First make f on lattice.
def latticed_f(position: Position) -> Value:
    x = [x_range[i][position[i]] for i in range(len(position))]
    return f(x)

# Set parameter of lattice_mcmc
chain_num = 2
tolerence = 0.01
lattice_size = [len(x_range[i]) for i in range(dim)]

# Test
t_begin = time()

mcmc_chains = lattice_mcmc.mcmc(chain_num, tolerence, lattice_size, latticed_f)

t_end = time()

print('time spent: ', t_end - t_begin)

for i in range(chain_num):
    print(  'End node of chain ' + str(i) + ': ',
            mcmc_chains[i][-1]
          )

# Return
# time spent:  0.010267972946166992
# End node of chain 0:  ([0, 0, 0, 0, 0], -0.0)
# End node of chain 1:  ([0, 0, 0, 0, 0], -0.0)

# So far so good.