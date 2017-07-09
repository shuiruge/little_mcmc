#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description
---------
Class of sampler by Metropolis algorithm.

Documentation
---------
C.f. `../doc/metropolis_sampler.tm`.
"""


import random
from math import log
from copy import deepcopy as copy


class MetropolisSampler:
    """
    An implementation of sampler by Metropolis algorithm.
    C.f. '/docs/metropolis_sampler.tm'.

    Args:

        iterations: int

        initialize_state: (None -> State)

        markov_process: (State -> State)

        burn_in: int

    Attributes:

        accept_ratio: float

            Generated only after calling `MetropolisSampler.sampling()`.

    Methods:

        sampling:

            Do the sampling by Metropolis algorithm.

    Remarks:

        The "State" can be any abstract class.
    """


    def __init__(
            self,
            iterations,
            initialize_state,
            markov_process,
            burn_in,
            log=True,
            ):

        self.iterations = iterations
        self.initialize_state = initialize_state
        self.markov_process = markov_process
        self.burn_in = burn_in
        self.log = log


    def sampling(self, log_target_distribution):
        """
        Do the sampling.

        Args:
            log_target_distribution: (State -> float)
                logarithm of target distribution.

        Returns:
            list of State, with length being iterations - burn_in.
        """

        init_state = self.initialize_state()

        if self.log:
            print('Initial state: {0}'.format(init_state))
        else:
            pass

        chain = [init_state]
        accepted = 0

        for i in range(self.iterations):

            next_state = self.markov_process(init_state)

            alpha = log_target_distribution(next_state) \
                  - log_target_distribution(init_state)
            u = log(random.uniform(0, 1))

            if alpha > u:

                accepted += 1
                chain.append(next_state)

                init_state = copy(next_state)

            else:

                chain.append(init_state)

        self.accept_ratio = accepted / self.iterations
        
        if self.log:
            print('Accept-ratio: {0}'.format(self.accept_ratio))
        else:
            pass

        return chain[self.burn_in:]
