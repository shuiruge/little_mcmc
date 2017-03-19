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
value of any given function on any given domain `A`.

This follows: https://github.com/Jverma/mcmc/blob/master/mcmc.py (c.f. also
https://github.com/Jverma/mcmc/blob/master/fitness.py)


Why Abstraction?
---------
This is the abstracted version of `lattice_mcmc.py`. This abstraction extracts
`random_move` out of `single_chain_mcmc` (comparing with that in
`lattice_mcmc.py`), since in some case, e.g. `NeuralNetwork`, the domain is
hard to be converted to lattice. Verily, in `NeuralNetwork`, the domain becomes
the "space of `NeuralNetwork`". That is, e.g.,
		
	random_move :: Space[NeuralNetwork] -> Space[NeuralNetwork];
	
	function :: Space[NeuralNetwork] -> Value.
	

#Parallel Computation of Chains
#---------
#Parallel computation does be faster, but when the number of chains is large
#enough, the `Pool` crashes. I have met this situation.
#
#Remark that the map of Python3 (not parallel_map) effectively slows down the
#computation. You shall employ `[f(_) for _ in x_list]` instead!

                                
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


from random import random


# Typing Hint
# ----------------------
from typing import List, Tuple, Mapping, TypeVar

A = TypeVar('A')
Value = float
ChainNode = Tuple[A, Value]
Chain = List[ChainNode]
# ----------------------


def relative_gain(old_value: float,
                  new_value: float
                  ) -> float:

    if new_value == 0 and old_value == 0:
        return 0
    else:
        return (new_value - old_value) / (abs(new_value) + abs(old_value))


def single_chain_mcmc(function: Mapping[A, float],
                      random_move: Mapping[A, A],
                      init_arg0: A,
                      tolerence=0.01,
                      max_break_counter=30,
                      iterations=10 ** 10,
                      ) -> Chain:
    """
    Find the argmax of function on by single chain MCMC.
    
    
    Parameters
    ---------
    `random_move`:
        It can be ANY function mapping from `A` to `A`. It's so named to
        analogy to Markov chain.
        
    `tolerence`:
        position alters when, at the next position, the relative gain
        of function exceeds `tolerence * random()`. This threshold
        is always positive, see 1 below.
    
    max_break_counter:
        see 2 below.
    
    1. Argument in `A` is altered ONlY when it gains a greater value of
       function.
    2. If it stays in one position for quite a long time (determined by
       `max_break_counter`), then break the iteration and finish the chain.
       And, the `max_break_counter` SHALL BE PROPORTIONAL TO DIMENSION OF `A`.
    """
    
    # Further restrict the arguments  
    assert tolerence > 0
        
    assert max_break_counter > 0
    
    assert iterations > 0
    
    # Do MCMC    
    init_arg = init_arg0.copy()
    init_value = function(init_arg)
    
    chain = [(init_arg, init_value)]
    
    break_counter = 0

    for step in range(iterations):
        new_arg = random_move(init_arg)
        new_value = function(new_arg)

        if relative_gain(init_value, new_value) > tolerence * random():
            break_counter = 0 # initialize break_counter.

            init_arg = new_arg.copy()
            init_value = new_value

            chain.append((new_arg, new_value))
            
        # Break if it stays on one position for quite a long time.
        # The breaking threshold shall be proportional to dimension.
        elif break_counter < max_break_counter:
            break_counter += 1
            
        else:
            break

    return chain


def best_chain(chain_list: List[Chain]) -> Chain:
    """ Select the chain with the highest value in its end-node.
    """
    
    best_chain = chain_list[0]
    best_end_node_value = best_chain[-1][1]
    
    for chain in range(chain_list):
        new_end_node_value = chain[-1][1]
        
        if new_end_node_value > best_end_node_value:
            best_chain = chain
            best_end_node_value = new_end_node_value
        
        else:
            pass
    
    return best_chain
