import random
import copy

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
			pass
	return allocs


def wdp(preferences, nomination, allocs, players_per_team):
	"""
	Input:
	* [preferences] List of dicts. Combinatorial preferences for each bidder.
	* [nomination] Set. Nominated bundle that must be allocated.
	* [allocs] List of lists. Each bidder's current allocation.
	* [players_per_team] Int.

	Output:
	* List of lists. Each bidder receives list of allocated players from bundle.
	"""
	# Maintain list of tuples. First elt is allocation, second elt is its value.
	poss_allocs = get_allocations(nomination, len(preferences))
	values = []

	def is_feasible(allocation):
		# TODO: Determine whether allocation is feasible.
		# Must check (1) there is enough room on team for package, (2) budget allows whatever VCG payment is.
		return True

	for i in range(poss_allocs):
		if is_feasible(poss_allocs[i]):
			values[i] = sum([preferences[i][bundle] for bundle in poss_allocs[i]])
		else:
			values[i] = None
	poss = [(poss_allocs[i], values[i]) for i in range(len(poss_allocs))]
	poss.sort(key = lambda x: -x[1])
	return poss[0][0]

def vcg_payment(preferences, nomination):
	"""
	Input: 
	* [preferences] List of dicts.
	* [nomination] Set.

	Output:
	* List of VCG payments. Each bidder receives a VCG payment.
	"""
	return


def get_allocations(objects, agents):
	"""
	Input:
	* [objects] List. Objects to allocate.
	* [agents] Int. Number of agents.

	Output:
	* List of list of lists. All possible allocations.
	"""
	all_allocations = [] # list of list of lists
	starting_allocation = []
	for i in range(agents):
		starting_allocation.append([])

	def recurse(current_allocation, index):
		if index == len(objects):
			all_allocations.append(current_allocation)
		else:
			for agent in range(agents):
				new_allocation = copy.deepcopy(current_allocation)
				new_allocation[agent].append(objects[index])
				recurse(new_allocation, index + 1)
		return 0

	recurse(starting_allocation, 0)
	return all_allocations

# def test_get_allocs():
# 	objects = [1, 2, 3]
# 	agents = 3
# 	all_allocations = get_allocations(objects, agents)
# 	for allocation in all_allocations:
# 		print allocation

# 	print len(all_allocations)
# 	return 0

# test_get_allocs()

