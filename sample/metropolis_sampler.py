"""
Description
------
1. A sampler by Metropolis algorithm.

2. The proposed transition distribution is Gaussian.

3. C.f. _An Introduction to MCMC for Machine Learning_, section 3.1.
"""

# Typing-hints
from typing import List, Tuple, Mapping
from random import uniform, gauss
from math import exp

Vector = List[float]
ChainNode = Tuple[Vector, float]
Chain = List[ChainNode]


def metropolis_sampler(
        target_distribution: Mapping[Vector, float],
        sigma: float,
        init_vector: Vector,
        iterations=5000,
        burn_in=100
        ) -> Chain:
    """
    Description
    ------
    1. A sampler by Metropolis algorithm.
    
    2. The proposed transition distribution is Gaussian.
    
    3. C.f. _An Introduction to MCMC for Machine Learning_, section 3.1.
    
    Inputs
    ------
    target_distribution:
        Any n-dimensional distribution. That is, any integratible non-negative
        function from $\mathbb{R}^n$ to $\mathbb{R}$.
    
    sigma:
        The sigma in the Gaussian proposed transition distribution.
    
    init_vector:
        Any vector in $\mathbb{R}^n$ in the support of the target_distribution.
    
    burn_in:
        We drop out all accepted samples before value of burn_in.
    
    Output
    ------
    [(sample_0, target_distribution(sample_0)),
     (sample_1, target_distribution(sample_1)),
     ...
     ]
    
    where sample_i is a n-dimensional vector.
    """

    chain = []
    accepted = 0


    def random_move(init_vector: Vector) -> Vector:
        next_vector = [c + gauss(0, sigma) for c in init_vector]
        return next_vector


    for step in range(iterations):

        # step 1, Markov process
        next_vector = random_move(init_vector)

        # step 2, acceptance
        init_target = target_distribution(init_vector)
        next_target = target_distribution(next_vector)

        alpha = min([1, next_target / init_target])

        u = uniform(0, 1)
        acceptQ = (alpha > u)

        # step 3, sampling and create chian-node
        if acceptQ:
            accepted += 1

            init_vector = next_vector.copy()
            init_target = next_target

            # Drop out first several samples
            if accepted > burn_in:
                chain.append((init_vector, init_target))
                
            else:
                pass

        else:
            pass
        
        # step 4, print accepted ratio in the end
        if step == iterations - 1:
            accepted_ratio = accepted / iterations
            print("accepted ratio = {0}".format(accepted_ratio))

    return chain
