# little_mcmc

Description
---------
This is a little module of bared MCMC algorithm, used for computing the maximum
value of any given function on any given range OF LATTICE in any given dimension
(for precise definition, see below).

This follows: https://github.com/Jverma/mcmc/blob/master/mcmc.py (c.f. also
https://github.com/Jverma/mcmc/blob/master/fitness.py)


Lattice and Position
---------
A n-dimensional lattice, depending on n positive integers `[N_1, ..., N_n]`,
is a list of positions; each position is of the form
    
    [x_1, x_2, ..., x_n]

where x_i is in range(N_i). The lattice, then, is a list of ALL such positions.


To-do
------
Needs optimization: when rejected while the new position does be higher than
that I'm standing on, this position shall be recorded in RAM, until in several
steps later my position becomes higher than it.

