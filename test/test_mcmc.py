import sys
sys.path.append('../sample/')
import mcmc


## Test
f = lambda x: 10 ** 2 - x[0] ** 2 - x[1] ** 2 - x[2] ** 2 - x[3] ** 2
tolerence = 0.001
chain_num = 1
lattice_size = [10000, 10000, 10000, 10000]
step_size = 1
max_break_counter = 30
## Test for `find_max_by_single_chain_mcmc_on_lattice`
init_position = [randint(0, _ - 1) for _ in lattice_size]
result = find_max_by_single_chain_mcmc_on_lattice(tolerence, lattice_size, f, init_position, max_break_counter, 10 ** 10, 1)
## If chain_positions are uncommented (also that within `find_max_by_single_chain_mcmc_on_lattice`)
print(len(chain_positions))
print(result['chain'][-1], result['accepted_ratio'])
## Test for find_max_on_lattice
print(find_max_on_lattice(chain_num, tolerence, lattice_size, f, max_break_counter = max_break_counter))
## so far so good.
'''
It is found that the `tolerence` shall NOT be large. E.g. for the previous tests:
    1. if set `tolerence, max_break_counter = 0.01, 30`, the chain won't move at
       all, since the threshold of moving is high and thus it's easy to reach
       the `max_break_counter`;
    2. so is setting `tolerence, max_break_counter = 0.1, 300`;
    3. if set `tolerence, max_break_counter = 0.1, 3000`, the chain moves for
       for quite a long time;
    4. if set `tolerence, max_break_counter = 0.01, 300`, the chain moves (for
       for quite a long time) and then returns the correct result;
    5. if set `tolerence, max_break_counter = 0.001, 30`, the chain moves and
       then returns the correct result, very quickly.
So, we find:
    1. for relatively large `tolerence`, the chain won't move since the
       threshold of moving is high and thus it's easy to reach the
       `max_break_counter`;
    2. even though, tuning `max_break_counter` to be larger solves this problem,
       it will take quite a long time to run.
    3. for relatively small `tolerence`, the chain moves return the correct
       result quickly, without a relatively large `max_break_counter`.
So, the safe and economic setting is using a relatively small but still
non-vanishing `tolerence`.
'''