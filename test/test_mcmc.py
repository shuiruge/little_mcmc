"""
This the test of `/sample/mcmc.py`. It's seeking the argmax of a function given
on lattice.

This can be seen as a re-construction of `/test/test_lattice_mcmc.py`.
"""


import sys
sys.path.append('../sample/')
import mcmc
from random import randint, gauss
from time import time


# Typing Hint
# ----------------------
from typing import List, Tuple

Position = List[int]
Value = float
ChainNode = Tuple[Position, Value]
Chain = List[ChainNode]
# ----------------------


def random_move0(lattice_size: List[int],
                position: Position,
                step_length: int
                ) -> Position:
    
    for num in lattice_size:
        assert num > 0
        
    assert len(lattice_size) == len(position)
    
    assert step_length > 0
    
    new_position = [_ + round(gauss(0, 1) * step_length) for _ in position]
    
    for dim in range(len(position)):
        # boundary cases:
        if new_position[dim] >= lattice_size[dim] or new_position[dim] < 0:
            new_position[dim] = position[dim]
        else:
            pass
    return new_position


dim = 5
lattice_size = [100 for i in range(dim)]

random_move = lambda position: random_move0(lattice_size, position, 1)

f = lambda x: - sum([__ ** 2 for __ in x])

t_begin = time()

mcmc_result = mcmc.single_chain_mcmc(
                        f, random_move,
                        [randint(0, 99) for i in range(dim)]
                        )

t_end = time()
print('time spent: ', t_end - t_begin)
print('(argmax, max): ', mcmc_result[-1])
# Return
# time spent:  0.00745391845703125
# (argmax, max):  ([0, 0, 0, 0, 0], 0)

# So far so good.
