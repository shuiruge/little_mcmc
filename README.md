little_mcmc
=========

Description
---------
This is a little module of bared MCMC algorithm, used for sampling, or then
computing the maximum value of any given function on any given domain of
any given dimension.

Reference
------
For "Metropolis sampler", c.f. _An Introduction to MCMC for Machine Learning_,
section 3.1.

For gaining global argmax, c.f. section 3.2 in the same paper.

To-do
------
Needs optimization: when rejected while the new position does be higher than
that I'm standing on, this position shall be recorded in RAM, until in several
steps later my position becomes higher than it.

