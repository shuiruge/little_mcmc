#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 20:08:26 2017

@author: shuiruge
"""

import random
from math import log
from copy import deepcopy as copy


class SAM:
    """
    Class of a "step-size adaptive Metropolis" sampler.
    
    Args:
        iterations: int

        initialize_state: (None -> [float]),
        
        init_step_size: float
        
        beta: float
            Parameter to adjust step-size.
        
        burn_in: int
    
    Attributes:

        accept_ratio: float

            Generated only after calling `SAM.sampling()`.

    Methods:

        sampling:

            Do the sampling by Metropolis algorithm.
    """
    
    def __init__(
            self,
            iterations,
            initialize_state,
            init_step_size,
            beta,
            burn_in
            ):

        self.iterations = iterations
        self.initialize_state = initialize_state
        self.init_step_size = init_step_size
        self.beta = beta
        self.burn_in = burn_in
        
        self.step_size = self.init_step_size

        
    
    def _markov_process(self, step_size, init_state):
        
        next_state = [
                x + random.gauss(0, step_size)
                for x in init_state
                ]
        
        return next_state
        
        


    def sampling(self, log_target_distribution):
        """
        Do the sampling.

        Args:
            log_target_distribution: ([float] -> float)
                logarithm of target distribution.

        Returns:
            list of [float], with length being iterations - burn_in.
        """

        init_state = self.initialize_state()
        print('Initial state: {0}'.format(init_state))

        chain = [init_state]
        accepted = 0
        self.step_size_list = [self.step_size]

        for i in range(self.iterations):

            next_state = self._markov_process(self.step_size, init_state)

            alpha = log_target_distribution(next_state) \
                  - log_target_distribution(init_state)
            u = log(random.uniform(0, 1))

            if alpha > u:

                accepted += 1
                chain.append(next_state)

                init_state = copy(next_state)
                
                # Update `self.step_size`
                self.step_size = self.init_step_size
                self.step_size_list.append(self.step_size)

            else:

                chain.append(init_state)
                
                # Update `self.step_size`
                power = random.gauss(0, self.beta)
                self.step_size *= 2 ** power
                self.step_size_list.append(self.step_size)
                

        self.accept_ratio = accepted / self.iterations
        print('Accept-ratio: {0}'.format(self.accept_ratio))

        return chain[self.burn_in:]
