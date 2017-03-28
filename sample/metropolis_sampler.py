"""
Description
------
1. A sampler by Metropolis algorithm.

2. The proposed transition distribution is Gaussian.

3. C.f. _An Introduction to MCMC for Machine Learning_, section 3.1.
"""

# Typing-hints
from typing import List, Tuple, Mapping
from random import uniform, gauss, randint
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
    
    2. The priori distribution is Gaussian.
    
    2.1 The "priori" is the proposed transition distribution. This terminology
        follows Metropolis et al (1953), indicating that this distribution
        is given before discriminating on the target_distribution.
    
    3. C.f. _An Introduction to MCMC for Machine Learning_, section 3.1.
    
    4. What is `gibbs` meaning for??? In practice, it does increases accepted
       ratio. But I do not know why.
    
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
    
    init_target = target_distribution(init_vector)
    assert init_target > 0
    
    def random_move(init_vector: Vector) -> Vector:
        
        next_vector = [ x + gauss(0, sigma)
                        for x in init_vector
                        ]
        return next_vector

    chain = [(init_vector, init_target)]
    accepted = 0
    
    for step in range(iterations):

        # step 1, Markov process
        next_vector = random_move(init_vector)

        # step 2, acceptance
        next_target = target_distribution(next_vector)
        alpha = min([1, next_target / init_target])

        u = uniform(0, 1)
        acceptQ = (alpha > u)

        # step 3, sampling and create chain-node
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
