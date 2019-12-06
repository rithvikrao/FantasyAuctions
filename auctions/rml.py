import random
import copy
import sys
from itertools import chain, combinations

def rml(num_players, num_bidders, players_per_team, max_bundle_size, budget, preferences):
	"""
	Input:
	* [num_players] Int.
	* [num_bidders] Int.
	* [players_per_team] Int.
	* [max_bundle_size] Int.
	* [budget] Int.
	* [preferences] List of dicts. Combinatorial preferences for each bidder. frozenset -> int
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
	
	random.shuffle(bidders)
	while sum([len(alloc) for alloc in allocs]) < players_per_team * num_bidders:

		for i in bidders:
			maxval = -sys.maxint
			maxbundle = None
			for item in preferences[i]:
				if len(preferences[i][item]) <= max_bundle_size and len(preferences[i][item]) <= players_per_team - len(allocs[i])and preferences[i][item] > maxval:
					maxval = preferences[i][item]
					maxbundle = item
			if maxbundle:
				subsets = powerset(max)
				valuations = [dict() for j in range(len(preferences))]
				for subset in subsets:
					for j in range(len(preferences)): # iterate over agents
						# bid for each sub-bundle of nominated bundle is the amount of value it adds to the team each agent already owns
						new_alloc = subset.union(allocs[j]) 
						added_value = preferences[j][new_alloc] - preferences[j][allocs[j]]
						valuations[j][subset] = min(added_value, budgets[j])
						# OLD STUFF
						# valuations[j][subset] = min(preferences[j][subset], budgets[j]) # old, if we don't think about already-owned players
				soln = wdp(valuations, maxbundle, allocs, players_per_team) # this is broken
			# TODO: update allocs with allocations of bundle items
			# TODO: update budgets for allocated bidders with VCG payment rule
	return allocs


def wdp(valuations, nomination, allocs, players_per_team):
	"""
	Input:
	* [valuations] List of dicts. Combinatorial valuations for each bidder.
	* [nomination] Set. Nominated bundle that must be allocated.
	* [allocs] List of lists. Each bidder's current allocation.
	* [players_per_team] Int.

	Output:
	* List of lists. Each bidder receives list of allocated players from bundle.
	"""
	poss_allocs = get_allocations(nomination, len(valuations))
	values = [None for i in range(len(poss_allocs))]

	def is_feasible(allocation):
		# Checks whether there is enough room on team for package
		for i in range(len(allocation)):
			if len(allocation[i]) > players_per_team - len(allocs[i]):
				return False
		return True

	for i in range(len(poss_allocs)):
		if is_feasible(poss_allocs[i]):
			# poss_allocs[i]
			values[i] = sum([valuations[j][poss_allocs[i][j]] for j in range(len(poss_allocs[i]))])

	poss = []

	# Remove all infeasible allocations
	for i in range(len(poss_allocs)):
		if values[i]:
			poss.append((poss_allocs[i], values[i]))

	poss.sort(key = lambda x: -x[1])
	if len(poss) == 0:
		raise ValueError("No feasible allocations of nominated bundle.")
	return poss[0][0]

def vcg_payments(valuations, nomination, winning_allocation, allocs, players_per_team):
	"""
	Input: 
	* [valuations] List of dicts. Each dict is frozenset -> int.
	* [nomination] Set. Bundle of players up for bidding.
	* [winning_allocation] List of frozensets. Frozenset at index i is bundle given to agent i.

	Output:
	* List of VCG payments. Each bidder receives a VCG payment.
	"""
	def get_others_value(allocation, this_agent):
		others_total = 0
		for j in range(num_agents):
			if j != this_agent:
				others_total += valuations[j][allocation[j]]
		return others_total

	num_agents = len(winning_allocation)
	payments = [] # list of length num_agents
	for i in range(num_agents): # compute payment of agent i
		others_total_value = get_others_value(winning_allocation, i)
		alternative_valuations = copy.deepcopy(valuations) # valuations if this agent dropped out (bid for all nonempty bundles is -infty)
		for bundle in alternative_valuations[i]:
			if len(bundle) > 0:
				alternative_valuations[i][bundle] = -sys.maxint
		alternative_allocation = wdp(alternative_valuations, nomination, allocs, players_per_team)
		# if len(alternative_allocation[i]) > 0: # this agent was allocated something even though we tried to remove her
		# 	raise ValueError("Error with computing VCG payments: Externality did not ignore current agent.")
		alternative_other_total_value = get_others_value(alternative_allocation, i)
		externality = alternative_other_total_value - others_total_value
		payments.append(externality)

	return payments


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
			for i in range(len(current_allocation)):
				current_allocation[i] = frozenset(current_allocation[i])
			all_allocations.append(current_allocation)
		else:
			for agent in range(agents):
				new_allocation = copy.deepcopy(current_allocation)
				new_allocation[agent].append(objects[index])
				recurse(new_allocation, index + 1)
		return 0

	recurse(starting_allocation, 0)
	return all_allocations

#def wdp(valuations, nomination, allocs, players_per_team):

# nomination is a frozenset
# return list of frozensets (list of subsets)
def powerset(nomination):
    s = list(nomination)
    subsets = list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))
    subset_list = []
    for subset in subsets:
    	subset_list.append(frozenset(subset))
    return subset_list

def test_wdp2():
	num_agents = 2
	players_per_team = 3
	allocs = [['e'], ['d']]
	nomination = ['a', 'b', 'c']
	# allocs = [[], []]
	# nomination = ['a', 'b', 'c']
	valuations = []
	subsets = [frozenset(['a']), frozenset(['b']), frozenset(['c']), frozenset(['a', 'b']), frozenset(['a', 'c']), frozenset(['b', 'c']), frozenset(['a', 'b', 'c']), frozenset([])]
	valuations.append({subsets[0]: 5, subsets[1]: 3, subsets[2]: 1, subsets[3]: 10, subsets[4]: 12, subsets[5]: 4, subsets[6]: 13, subsets[7]: 0})
	valuations.append({subsets[0]: 1, subsets[1]: 4, subsets[2]: 5, subsets[3]: 4, subsets[4]: 6, subsets[5]: 8, subsets[6]: 9, subsets[7]: 0})
	win = wdp(valuations, nomination, allocs, players_per_team)
	payments = vcg_payments(valuations, nomination, win, allocs, players_per_team)
	print win
	print payments
	return 0

#test_wdp2()

def test_wdp3():
	num_agents = 3
	players_per_team = 3
	allocs = [[], [], []]
	nomination = ['a', 'b', 'c']
	# allocs = [[], []]
	# nomination = ['a', 'b', 'c']
	valuations = []
	subsets = [frozenset(['a']), frozenset(['b']), frozenset(['c']), frozenset(['a', 'b']), frozenset(['a', 'c']), frozenset(['b', 'c']), frozenset(['a', 'b', 'c']), frozenset([])]
	valuations.append({subsets[0]: 5, subsets[1]: 3, subsets[2]: 1, subsets[3]: 10, subsets[4]: 12, subsets[5]: 4, subsets[6]: 13, subsets[7]: 0})
	valuations.append({subsets[0]: 1, subsets[1]: 4, subsets[2]: 5, subsets[3]: 4, subsets[4]: 6, subsets[5]: 8, subsets[6]: 9, subsets[7]: 0})
	valuations.append({subsets[0]: 1, subsets[1]: 5, subsets[2]: 1, subsets[3]: 7, subsets[4]: 5, subsets[5]: 8, subsets[6]: 9, subsets[7]: 0})
	win = wdp(valuations, nomination, allocs, players_per_team)
	payments = vcg_payments(valuations, nomination, win, allocs, players_per_team)
	print win
	print payments
	return 0

test_wdp3()


def test_powerset():
	nomination = frozenset(['a', 'b', 'c'])
	print powerset(nomination)
	return 0

#test_powerset()



def test_get_allocs():
	objects = [1, 2, 3]
	agents = 3
	all_allocations = get_allocations(objects, agents)
	for allocation in all_allocations:
		print allocation

	print len(all_allocations)
	return 0

# test_get_allocs()

