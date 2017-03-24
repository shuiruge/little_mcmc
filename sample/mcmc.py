
from typing import List, Tuple, Mapping, TypeVar
from random import uniform


A = TypeVar('A')
Value = float
Chain = List[Tuple[A, float]]


def metropolis(f: Mapping[A, float],
               random_move: Mapping[A, A],
               init_x: A,
               iterations: int,
               burn_in: int
               ) -> Chain:
    """
    Ensure that probabilities of `random_move(a) == b` and `random_move(b) == a`
    are equal. This is the condition of Metropolis algorithm. Or, the generalized
    algorithm, i.e. the Metropolis-Hastings algorithm, shall be employed.
    
    What does 'burn_in' mean???
    """
    assert f(init_x) > 0
    
    chain = []
    accepted = 0
    
    for step in range(iterations):
        
        # step 1, random movement
        next_x = random_move(init_x)
        
        # step 2, random acceptance
        init_value = f(init_x)
        next_value = f(next_x)
        
        if next_value < 0:
            print("{0}({1}) < 0.".format(f, next_x))
        
        else:
            alpha = next_value / init_value
            if alpha > uniform(0, 1):
                accepted += 1
                
                init_x = next_x.copy()
                init_value = next_value
                
                if accepted > burn_in:
                    chain.append((init_x, init_value))
                
                else:
                    pass
                
            else:
                pass
        
        if step == iterations - 1:
            accepted_ratio = accepted / iterations
            print("accepted ratio = {0}".format(accepted_ratio))
        
        else:
            pass
        
    return chain


# test
import numpy as np
from random import gauss

def f(x):
    return np.exp(- np.dot(x, x))


def random_move(x0, step_length=0.5):
    x = x0.copy()
    
    delta_x_lst = [gauss(0, 1) * step_length for i in range(x.ndim)]
    delta_x = np.array(delta_x_lst)
    
    return x + delta_x
    
c = metropolis(f, random_move, 5 * np.array([random() for i in range(100)]), 10 ** 6, 1000)


n = np.argmax([c[_][1] for _ in range(len(c))])
print(n, c[n])


import matplotlib.pyplot as plt

plt.plot([c[_][1] for _ in range(0, len(c), round(len(c) / 100))])
plt.show

## Extemely slow, and hard to convergent!