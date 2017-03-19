# -*- coding: utf-8 -*-
"""
To-do
------
Needs optimization: when rejected while the new position does be higher than
that I'm standing on, this position shall be recorded in RAM, until in several
steps later my position becomes higher than it.


Description
---------
This is a little module of bared MCMC algorithm, used for computing the maximum
value of any given function on any given range OF LATTICE in any given dimension
(for precise definition, see below).

This follows: https://github.com/Jverma/mcmc/blob/master/mcmc.py (c.f. also
https://github.com/Jverma/mcmc/blob/master/fitness.py)

This can be seen as an examplified version of the abstracted `mcmc.py`.

Lattice and Position
---------
A n-dimensional lattice, depending on n positive integers `[N_1, ..., N_n]`,
is a list of positions; each position is of the form

    [x_1, x_2, ..., x_n]

where x_i is in range(N_i). The lattice, then, is a list of ALL such positions.


Parallel Computation of Chains
---------
CAUTION: When the number of chains is large, please avoid setting
        `parallelQ = True` in `mcmc`!

Parallel computation does be faster, but when the number of chains is large
enough, the `Pool` crashes. I have met this situation.

Remark that the map of Python3 (not parallel_map) effectively slows down the
computation. You shall employ `[f(_) for _ in x_list]` instead!

                                
Test Result
---------
It is found that the `tolerence` shall NOT be large. E.g. for the tests in the
end of this file:
    
    1. if set `tolerence, max_break_counter = 0.01, 30`, the chain won't move at
       all, since the threshold of moving is high and thus it's easy to reach
       the `max_break_counter`;
       
    2. so is setting `tolerence, max_break_counter = 0.1, 300`;
    
    3. if set `tolerence, max_break_counter = 0.1, 3000`, the chain moves for
       for quite a long time;
       
    4. if set `tolerence, max_break_counter = 0.01, 300`, the chain moves (for
       for quite a long time) and then returns the correct result;
    
    5. if set `tolerence, max_break_counter = 0.001, 30`, the chain moves and
       then returns the correct result, very quickly.
       
So, we find:
    
    1. for relatively large `tolerence`, the chain won't move since the
       threshold of moving is high and thus it's easy to reach the
       `max_break_counter`;
       
    2. even though, tuning `max_break_counter` to be larger solves this problem,
       it will take quite a long time to run.
       
    3. for relatively small `tolerence`, the chain moves return the correct
       result quickly, without a relatively large `max_break_counter`.
       
So, the safe and economic setting is using a relatively small but still
non-vanishing `tolerence`.
"""


from random import gauss, random, randint
from multiprocessing.dummy import Pool


# Typing Hint
# ----------------------
from typing import List, Callable, Tuple, Mapping, Any

Position = List[int]
Value = float
ChainNode = Tuple[Position, Value]
Chain = List[ChainNode]
# ----------------------


def random_move(lattice_size: List[int],
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


def relative_gain(old_value: float,
                  new_value: float
                  ) -> float:

    if new_value == 0 and old_value == 0:
        return 0
    else:
        return (new_value - old_value) / (abs(new_value) + abs(old_value))


def single_chain_mcmc(tolerence: float, 
                      lattice_size: List[int],
                      function: Mapping[Position, float],
                      init_position0: Position,
                      max_break_counter=30,
                      iterations=10 ** 10,
                      step_length=1
                      ) -> Chain:
    """
    Find the argmax of function on lattice by single chain MCMC method.
    
    
    Parameters
    ---------
    `tolerence`:
        position alters when, at the next position, the relative gain
        of function exceeds `tolerence * random()`. This threshold
        is always positive, see 1 below.
                 
    `lattice_size`:
        e.g. [10, 5] represents a two-dimensional lattice with 10
        points on the first axis and 5 on the second.
                    
    `function`:
        maps from a position on lattice to a real.
    
    step_length:
        position alters, if possible, at step length
        `round(step_length * gauss(0, 1))`
                 
    max_break_counter:
        see 2 below.
    
    1. Position on lattice is altered ONlY when it gains a greater value of
       function.
    2. If it stays in one position for quite a long time (determined by
       `max_break_counter`), then break the iteration and finish the chain.
       And, the breaking threshold shall be proportional to dimension.
    """
    
    # Further restrict the arguments  
    assert tolerence > 0
    
    for num in lattice_size:
        assert num > 0
        
    assert len(lattice_size) == len(init_position0)
    
    for i in range(len(init_position0)):
        assert init_position0[i] >= 0
        assert init_position0[i] <= lattice_size[i] - 1

    assert max_break_counter > 0
    
    assert iterations > 0

    assert step_length > 0
    
    # Do MCMC
    dim = len(lattice_size)
    
    init_position = init_position0.copy()
    init_value = function(init_position)
    
    chain = [(init_position, init_value)]
    
    break_counter = 0

    for step in range(iterations):
        new_position = random_move(lattice_size, init_position, step_length)
        new_value = function(new_position)

        if relative_gain(init_value, new_value) > tolerence * random():
            break_counter = 0 # initialize break_counter.

            init_position = new_position.copy()
            init_value = new_value

            chain.append((new_position, new_value))
            
        # Break if it stays on one position for quite a long time.
        # The breaking threshold shall be proportional to dimension.
        elif break_counter < max_break_counter * dim:
            break_counter += 1
            
        else:
            break

    return chain


def random_position(lattice_size: List[int]) -> Position:
    return [randint(0, __ - 1) for __ in lattice_size]


def parallel_map(f: Mapping[Any, Any], lst: List[Any]):
    # Make the Pool of workers
    pool = Pool()
    result = pool.map(f, lst)

    #close the pool and wait for the work to finish
    pool.close()
    pool.join()

    return result


def mcmc(chain_num: int,
         tolerence: float,
         lattice_size: List[int],
         function: Mapping[Position, float],
         max_break_counter=30,
         iterations=10 ** 10,
         step_length=1,
         parallelQ=False
         ) -> List[Chain]:
    """ Find the argmax of function on lattice by single chain MCMC method.
    
    
    Parameters
    ---------
    `tolerence`:
        position alters when, at the next position, the relative gain
        of function exceeds `tolerence * random()`. This threshold
        is always positive, see 1 below.
                 
    `lattice_size`:
        e.g. [10, 5] represents a two-dimensional lattice with 10
        lattice-point on the first axis and 5 on the second.
                    
    `function`:
        maps from a position on lattice to a real.
    
    step_length:
        position alters, if possible, at step length
        `round(step_length * gauss(0, 1))`
                 
    max_break_counter:
        see 2 below.
    
    1. Position on lattice is altered ONlY when it gains a greater value of
       function.
    2. If it stays in one position for quite a long time (determined by
       `max_break_counter`), then break the iteration and finish the chain.
       And, the breaking threshold shall be proportional to dimension.
    """
    # Further restrict the arguments  
    assert tolerence > 0
    
    for num in lattice_size:
        assert num > 0
    
    assert max_break_counter > 0
    
    assert iterations > 0

    assert step_length > 0
    
    # Do MCMC
    init_position_list = [random_position(lattice_size) for __ in range(chain_num)]
    
    def f(init_position):
        return single_chain_mcmc(tolerence, lattice_size, function,
                                 init_position, max_break_counter,
                                 iterations, step_length
                                 )
        
    if parallelQ == True:
        # parallely run mcmc for each chain
        mcmc_chains = parallel_map(f, init_position_list)
        
    else:
        mcmc_chains = [f(__) for __ in init_position_list]
        # Instead, list(map(f, init_position_list)) is quite slow!

    return mcmc_chains


def best_chain(chain_list: List[Chain]) -> Chain:
    """ Select the chain with the highest value in its end-node.
    """
    
    best_chain = chain_list[0]
    best_end_node_value = best_chain[-1][1]
    
    for chain in range(chan_list):
        new_end_node_value = chain[-1][1]
        
        if new_end_node_value > best_end_node_value:
            best_chain = chain
            best_end_node_value = new_end_node_value
        
        else:
            pass
    
    return best_chain
