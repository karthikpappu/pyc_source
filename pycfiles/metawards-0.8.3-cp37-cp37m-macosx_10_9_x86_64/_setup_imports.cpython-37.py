# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/iterators/_setup_imports.py
# Compiled at: 2020-04-20 09:02:59
# Size of source mod 2**32: 3316 bytes
from .._network import Network
from .._population import Population
__all__ = [
 'setup_seed_specified_ward',
 'setup_seed_all_wards',
 'setup_seed_wards']

def setup_seed_specified_ward(network: Network, infections, play_infections, **kwargs):
    """Setup function that sets up the Network by seeding the infection
       at the ward specified by looking up the ward index
       from network.to_seed using index params.ward_seed_index

       Parameters
       ----------
       network: Network
         The network to be seeded
       infections
         Space to hold the 'work' infections
       play_infections
         Space to hold the 'play' infections
       kwargs
         Arguments that are not used by this setup function
    """
    wards = network.nodes
    links = network.to_links
    params = network.params
    seed_index = int(params.ward_seed_index)
    seed = network.to_seed[seed_index]
    print(f"Setup by seeding the ward at index {seed}")
    j = 0
    while links.ito[j] != seed or links.ifrom[j] != seed:
        j += 1

    if links.suscept[j] < params.initial_inf:
        wards.play_suscept[seed] -= params.initial_inf
        play_infections[0][seed] += params.initial_inf
    infections[0][j] = params.initial_inf
    links.suscept[j] -= params.initial_inf


def setup_seed_all_wards(network: Network, population: Population, infections, play_infections, **kwargs):
    """Seed the wards with an initial set of infections, assuming
       an 'expected' number of infected people out of a population
       of 'population', based on the number of daily imports held
       in params.daily_imports
    """
    wards = network.nodes
    params = network.params
    print('Setup by seeding all wards')
    frac = float(params.daily_imports) / float(population.initial)
    for i in range(0, network.nnodes + 1):
        temp = wards.denominator_n[i] + wards.denominator_p[i]
        to_seed = int(frac * temp + 0.5)
        wards.play_suscept[i] -= to_seed
        play_infections[0][i] += to_seed


def setup_seed_wards(network: Network, **kwargs):
    """Seed the wards with an initial infection. If a specific ward
       has been highlighted via `params.ward_seed_index`, then this
       will be seeded using the function `setup_seed_specified_ward`.
       Otherwise, all wards will be seeded via `setup_seed_all_wards`.

       Parameters
       ----------
       network: Network
         The network over which the model will run
       kwargs
         Arguments not needed for this function
    """
    params = network.params
    try:
        seed_index = int(params.ward_seed_index)
    except Exception:
        seed_index = None

    if seed_index is None:
        setup_seed_all_wards(network=network, **kwargs)
    else:
        setup_seed_specified_ward(network=network, **kwargs)