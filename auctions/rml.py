import random

def rml(num_bidders, players_per_team, max_bundle_size, budget):
	"""
	Input:
	* [num_bidders] Int.
	* [players_per_team] Int.
	* [max_bundle_size] Int.
	# [budget] Int.
	* Dynamic bundle input. Bidder queried for nomination bundle at each timestep.

	Output:
	* List of lists. Each bidder receives list of allocated players.
	"""

	bidders = [i for i in range(num_bidders)]
	allocs = [[] for i in range(num_bidders)]
	budgets = [budget for i in range(num_bidders)]

	while sum([len(alloc) for alloc in allocs]) < players_per_team * num_bidders:
		random.shuffle(bidders)
		for i in range(len(bidders)):
			nomination = input(f"Bidder {i}, state your nominated bundle:")
			# TODO: ensure input is formatted correctly (handle TypeError)
			# TODO: ensure nominated bundle is smaller than max_bundle_size
			# TODO: for each combination of items in bundle:
				# TODO: query all users for value only on permutations that are still feasible for them
				# TODO: ensure input is formatted correctly
				# TODO: ensure users have enough budget (negative bids okay)
			# TODO: solve WDP on bundle with these values
			# TODO: update allocs with allocations of bundle items
			# TODO: update budgets for allocated bidders with VCG payment rule
	return allocs