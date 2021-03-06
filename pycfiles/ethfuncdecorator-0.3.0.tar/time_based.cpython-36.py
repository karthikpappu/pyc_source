# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/gas_strategies/time_based.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 6371 bytes
import collections, math, operator
from eth_utils import to_tuple
from web3.utils.toolz import curry, groupby, sliding_window
MinerData = collections.namedtuple('MinerData', ['miner', 'num_blocks', 'min_gas_price'])
Probability = collections.namedtuple('Probability', ['gas_price', 'prob'])

def _get_avg_block_time(w3, sample_size):
    latest = w3.eth.getBlock('latest')
    if latest['number'] == 0 or sample_size == 0:
        return 0
    else:
        constrained_sample_size = min(sample_size, latest['number'])
        oldest = w3.eth.getBlock(latest['number'] - constrained_sample_size)
        return (latest['timestamp'] - oldest['timestamp']) / constrained_sample_size


def _get_raw_miner_data(w3, sample_size):
    latest = w3.eth.getBlock('latest', full_transactions=True)
    for transaction in latest['transactions']:
        yield (latest['miner'], latest['hash'], transaction['gasPrice'])

    block = latest
    for _ in range(sample_size - 1):
        if block['number'] == 0:
            break
        block = w3.eth.getBlock((block['parentHash']), full_transactions=True)
        for transaction in block['transactions']:
            yield (
             block['miner'], block['hash'], transaction['gasPrice'])


def _aggregate_miner_data(raw_data):
    data_by_miner = groupby(0, raw_data)
    for miner, miner_data in data_by_miner.items():
        _, block_hashes, gas_prices = map(set, zip(*miner_data))
        yield MinerData(miner, len(set(block_hashes)), min(gas_prices))


@to_tuple
def _compute_probabilities(miner_data, wait_blocks, sample_size):
    """
    Computes the probabilities that a txn will be accepted at each of the gas
    prices accepted by the miners.
    """
    miner_data_by_price = tuple(sorted(miner_data,
      key=(operator.attrgetter('min_gas_price')),
      reverse=True))
    for idx in range(len(miner_data_by_price)):
        min_gas_price = miner_data_by_price[idx].min_gas_price
        num_blocks_accepting_price = sum(m.num_blocks for m in miner_data_by_price[idx:])
        inv_prob_per_block = (sample_size - num_blocks_accepting_price) / sample_size
        probability_accepted = 1 - inv_prob_per_block ** wait_blocks
        yield Probability(min_gas_price, probability_accepted)


def _compute_gas_price(probabilities, desired_probability):
    """
    Given a sorted range of ``Probability`` named-tuples returns a gas price
    computed based on where the ``desired_probability`` would fall within the
    range.

    :param probabilities: An iterable of `Probability` named-tuples sorted in reverse order.
    :param desired_probability: An floating point representation of the desired
        probability. (e.g. ``85% -> 0.85``)
    """
    first = probabilities[0]
    last = probabilities[(-1)]
    if desired_probability >= first.prob:
        return first.gas_price
    if desired_probability <= last.prob:
        return last.gas_price
    for left, right in sliding_window(2, probabilities):
        if desired_probability < right.prob:
            continue
        else:
            if desired_probability > left.prob:
                raise Exception('Invariant')
        adj_prob = desired_probability - right.prob
        window_size = left.prob - right.prob
        position = adj_prob / window_size
        gas_window_size = left.gas_price - right.gas_price
        gas_price = int(math.ceil(right.gas_price + gas_window_size * position))
        return gas_price
    else:
        raise Exception('Invariant')


@curry
def construct_time_based_gas_price_strategy(max_wait_seconds, sample_size=120, probability=98):
    """
    A gas pricing strategy that uses recently mined block data to derive a gas
    price for which a transaction is likely to be mined within X seconds with
    probability P.

    :param max_wait_seconds: The desired maxiumum number of seconds the
        transaction should take to mine.
    :param sample_size: The number of recent blocks to sample
    :param probability: An integer representation of the desired probability
        that the transaction will be mined within ``max_wait_seconds``.  0 means 0%
        and 100 means 100%.
    """

    def time_based_gas_price_strategy(web3, transaction_params):
        avg_block_time = _get_avg_block_time(web3, sample_size=sample_size)
        wait_blocks = int(math.ceil(max_wait_seconds / avg_block_time))
        raw_miner_data = _get_raw_miner_data(web3, sample_size=sample_size)
        miner_data = _aggregate_miner_data(raw_miner_data)
        probabilities = _compute_probabilities(miner_data,
          wait_blocks=wait_blocks,
          sample_size=sample_size)
        gas_price = _compute_gas_price(probabilities, probability / 100)
        return gas_price

    return time_based_gas_price_strategy


fast_gas_price_strategy = construct_time_based_gas_price_strategy(max_wait_seconds=60,
  sample_size=120)
medium_gas_price_strategy = construct_time_based_gas_price_strategy(max_wait_seconds=600,
  sample_size=120)
slow_gas_price_strategy = construct_time_based_gas_price_strategy(max_wait_seconds=3600,
  sample_size=120)
glacial_gas_price_strategy = construct_time_based_gas_price_strategy(max_wait_seconds=86400,
  sample_size=720)