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
value of any given function in any given range in any dimension.

This follows: https://github.com/Jverma/mcmc/blob/master/mcmc.py (c.f. also
https://github.com/Jverma/mcmc/blob/master/fitness.py)

Parallel Computation of Chains
---------
CAUTION: When the number of chains is large, please avoid setting
        `parallelQ = True` in `find_max_by_mcmc_on_lattice`!
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

def random_move(lattice_size, position, step_length):
    """ [Int] * [Int] -> [Int]
    """
    new_position = [_ + round(gauss(0, 1) * step_length) for _ in position]
    
    for dim in range(len(position)):
        # boundary cases:
        if new_position[dim] >= lattice_size[dim] or new_position[dim] < 0:
            new_position[dim] = position[dim]

    return new_position


def relative_gain(old_value, new_value):
    """ Real * Real -> Real
    """
    if new_value == 0 and old_value == 0:
        return 0
    else:
        return (new_value - old_value) / max(abs(new_value), abs(old_value))


def find_max_by_single_chain_mcmc_on_lattice(tolerence, lattice_size, function, init_position0, max_break_counter, iterations, step_length):
    """ Real * [Int] * ([Int] -> Real) * [Int] * Int * Int * Int -> {'chain': [[[Int], Real]], 'accepted_ratio': Real}
    
    Parameters
    ---------
    `tolerence`: position alters when, at the next position, the relative gain
                 of function exceeds `tolerence * random()`. This threshold
                 is always positive, see 1 below.
                 
    `lattice_size`: e.g. [10, 5] represents a two-dimensional lattice with 10
                    points on the first axis and 5 on the second.
                    
    `function`:  maps from a position on lattice to a real.
    
    step_length: position alters, if possible, at step length
                 `round(step_length * gauss(0, 1))`
                 
    max_break_counter: see 2 below.
    
    C.f. `find_max_by_one_chain_mcmc_on_lattice`:
    1. Position on lattice is altered ONlY when it gains a greater value of
       function.
    2. If it stays in one position for quite a long time (determined by
       `max_break_counter`), then break the iteration and finish the chain.
       And, the breaking threshold shall be proportional to dimension.
    """
    init_position = init_position0.copy()
    init_function_value = function(init_position)
    
    chain_trajectory = [[init_position, init_function_value]]
    
    accepted_points = 0
    break_counter = 0

    for step in range(iterations):
        new_position = random_move(lattice_size, init_position, step_length)
        new_function_value = function(new_position)

        #chain_positions.append(new_position) # for testing only.        
        if relative_gain(init_function_value, new_function_value) > tolerence * random():
            break_counter = 0 # initialize break_counter.
            accepted_points += 1

            init_position = new_position.copy()
            init_function_value = new_function_value

            chain_trajectory.append([init_position, init_function_value])
        # Break if it stays on one position for quite a long time.
        # The breaking threshold shall be proportional to dimension.
        elif break_counter <= max_break_counter * len(lattice_size):
            break_counter += 1
        else:
            break

    accepted_ratio = float(accepted_points / iterations)
    return {'chain': chain_trajectory, 'accepted_ratio': accepted_ratio}


def parallel_map(f, lst):
    """ (a -> b) * [a] -> [b]
    """
    # Make the Pool of workers
    pool = Pool()
    result = pool.map(f, lst)

    #close the pool and wait for the work to finish
    pool.close()
    pool.join()

    return result


def find_max_on_lattice(chain_num, tolerence, lattice_size, function, max_break_counter = 30, iterations = 10 ** 10, step_length = 1, parallelQ = False, output_chains = False):
    """ Int * Real * [Int] * ([Int] -> Real) -> [[Int], Real]

    CAUTION: When the number of chains is large, please avoid setting
            `parallelQ = True` in `find_max_by_mcmc_on_lattice`!
    Parallel computation does be faster, but when the number of chains is large
    enough, the `Pool` crashes. I have met this situation.
    
    Parameters
    ---------
    tolerence:   position alters when, at the next position, the relative gain
                 of function exceeds `tolerence * random()`. This threshold
                 is always positive, see 1 below.
    lattice_size: e.g. [10, 5] represents a two-dimensional lattice with 10
                    points on the first axis and 5 on the second.
    function:    maps from a position on lattice to a real.
    step_length: position alters, if possible, at step length
                 `round(step_length * gauss(0, 1))`.
    iterations: since we have set max_break_counter, iteration can be as large
                as possible, without worrying about iterating for too many times.
    max_break_counter: see 2 below.
    
    Outputs
    ------
    [best_position_on_lattice, its_function_value]
    
    Reference
    ---------    
    C.f. `find_max_by_one_chain_mcmc_on_lattice`:
    1. Position on lattice is altered ONlY when it gains a greater value of
       function.
    2. If it stays in one position for quite a long time (determined by
       `max_break_counter`), then break the iteration and finish the chain.
       And, the breaking threshold shall be proportional to dimension.
    """
    # generate init_position_list
    init_position_list = []
    for chain in range(chain_num):
        init_position = [randint(0, _ - 1) for _ in lattice_size]
        init_position_list.append(init_position)
    
    def single_chain_mcmc(init_position):
        """ [Real] -> {'chain': [[Int]], 'accepted_ratio': Real}
        """
        return find_max_by_single_chain_mcmc_on_lattice(tolerence, lattice_size, function, init_position, max_break_counter, iterations, step_length)

    if parallelQ == True:
        # parallely run mcmc for each chain
        mcmc_chains = parallel_map(single_chain_mcmc, init_position_list)
    else:
        mcmc_chains = [single_chain_mcmc(_) for _ in init_position_list] # Instead, list(map(f, init_position_list)) is quite slow!

    if output_chains == True:
        return mcmc_chains
    
    else:   
        # select out best one in these chains and get its end position
        best_position = mcmc_chains[0]['chain'][-1]
        function_value = function(best_position)
        
        for chain in range(chain_num):
            new_best_position = mcmc_chains[chain]['chain'][-1]
            new_function_value = function(new_best_position)
            if new_function_value > function_value:
                best_position = new_best_position.copy()
                function_value = new_function_value
        
        return [best_position, function_value]
            
                
        