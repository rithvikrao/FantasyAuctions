import random

def rml(num_players, num_bidders, players_per_team, max_bundle_size, budget, preferences):
	"""
	Input:
	* [num_players] Int.
	* [num_bidders] Int.
	* [players_per_team] Int.
	* [max_bundle_size] Int.
	* [budget] Int.
	* [preferences] List of dicts. Combinatorial preferences for each bidder.
	* Dynamic bundle input. Bidder queried for nomination bundle at each timestep.

	Output:
	* List of lists. Each bidder receives list of allocated players.
	"""

	# Bidders are 0-indexed
	bidders = [i for i in range(num_bidders)]

	# Allocation per bidder
	allocs = [[] for i in range(num_bidders)]

	# Set of allocated players
	allocated = set()

	# Each bidder has the same budget
	budgets = [budget for i in range(num_bidders)]

	while sum([len(alloc) for alloc in allocs]) < players_per_team * num_bidders:
		random.shuffle(bidders)
		for i in range(len(bidders)):
			# TODO: extract nominated bundle from bidder i's preferences
			# TODO: ensure nominated bundle is smaller than max_bundle_size AND nominating player has space for size of bundle
			# TODO: solve WDP on bundle with these values
			# TODO: update allocs with allocations of bundle items
			# TODO: update budgets for allocated bidders with VCG payment rule
	return allocs


def wdp(preferences, nomination):
	"""
	Input:
	* [preferences] List of dicts. Combinatorial preferences for each bidder.
	* [nomination] Set. Nominated bundle that must be allocated.

	Output:
	* List of lists. Each bidder receives list of allocated players from bundle.
	"""
	# Maintain list of tuples. First elt is allocation, second elt is its value.
	poss = partition(nomination)

	return

def vcg_payment(preferences, nomination):
	"""
	Input: 
	* [preferences] List of dicts.
	* [nomination] Set.

	Output:
	* List of VCG payments. Each bidder receives a VCG payment.
	"""
	return

# Stolen from https://stackoverflow.com/questions/19368375/set-partitions-in-python
def partition(collection):
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset 
        yield [ [ first ] ] + smaller
