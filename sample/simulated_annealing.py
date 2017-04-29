#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description
---------
Python3 code of simulated annealing algorithm. This algorithm is to get the
argmin of any target function on any domain. We call the domain the space of
"state" where "state" represents any abstract class.

C.f. `../doc/simulated_annealing.tm`.
"""

import numpy as np
from metropolis_sampler import MetropolisSampler


class Temperature:

    def __init__(self, temperature_of_time):
        """ (int -> float) -> None

            The "temperature of time" means temperature(time), where the "time"
            runs over 0, 1, 2, ..., max_time.
        """

        self.temperature_of_time = temperature_of_time

        self.iterator = -1


    def __call__(self):

        self.iterator += 1

        return self.temperature_of_time(self.iterator)


class SimulatedAnnealing(object):

    def __init__(self, temperature_of_time,
                iterations, initialize_state, markov_process
                ):
        """ (int -> float) * int * (None -> State) * (State -> State) -> None

            The "State" can be any abstract class.

            Caution
            ------
            The iterations cannot exceed the max_time in temperature_of_time.
        """

        ## Argument of Temperature
        self.temperature_of_time = temperature_of_time

        ## Argument of MetropolisSampler
        self.iterations = iterations
        self.initialize_state = initialize_state
        self.markov_process = markov_process

    def __call__(self, target_function):
        """ (State -> float) -> State
        """

        temperature = Temperature(self.temperature_of_time)

        def target_distribution(state):

            return np.exp(-1 * target_function(state) / temperature())

        metropolis_sampler = MetropolisSampler(
                self.iterations, self.initialize_state, self.markov_process
                )

        chain = metropolis_sampler(target_distribution)

        self.chain = chain

        return chain[-1]

