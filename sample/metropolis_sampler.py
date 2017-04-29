#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description
---------
C.f. `../doc/metropolis_sampler.tm`.
"""

import random

class MetropolisSampler:

    def __init__(self, iterations, initialize_state, markov_process):
        """ int * (None -> State) * (State -> State) -> None

            The "State" can be any abstract class.
        """
        self.iterations = iterations
        self.initialize_state = initialize_state
        self.markov_process = markov_process

    def __call__(self, target_distribution):
        """ (State -> float) -> [State]
        """

        init_state = self.initialize_state()
        assert target_distribution(init_state) > 0

        chain = [init_state]
        accepted = 0

        for i in range(self.iterations):

            next_state = self.markov_process(init_state)

            alpha = target_distribution(next_state) / target_distribution(init_state)
            u = random.uniform(0, 1)

            if alpha > u:

                accepted += 1
                chain.append(next_state)

                init_state = next_state.copy()

            else:
                pass

        accept_ratio = accepted / self.iterations
        print('accept-ratio = {0}'.format(accept_ratio))

        return chain
