little_mcmc
=========

Description
---------
This is a little module of bared MCMC algorithm, used for computing the maximum
value of any given function on any given domain of any given dimension.

This follows: https://github.com/Jverma/mcmc/blob/master/mcmc.py (c.f. also
https://github.com/Jverma/mcmc/blob/master/fitness.py)


To-do
------
Needs optimization: when rejected while the new position does be higher than
that I'm standing on, this position shall be recorded in RAM, until in several
steps later my position becomes higher than it.

