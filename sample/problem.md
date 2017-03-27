Problem
======

1. As follow:
  
  1. Increasing the `sigma` in `metropolis_sampler` will decrease `accepted_ratio`. But will help jump out of a local maximum in a finite number of `iterations`.
  
  2. Decreasing the `sigma` in `metropolis_sampler` will increase `accepted_ratio`. But will also decrease the probability of jumping out a local maximum in a finite number of `iterations`.
