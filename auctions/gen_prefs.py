import random
import itertools
import math

# Generate preferences across all agents
def generate_preferences(singletons, num_agents, team_size):
	# Base values across all singleton players
	base_values = {singleton: random.randint(0, 100) for singleton in singletons}
	base_pairwise_perturbations = {}

	for i in range(len(singletons)):
		for j in range(i + 1, len(singletons)):
			base_pairwise_perturbations[frozenset([singletons[i], singletons[j]])] = random.randint(-10, 10)

	# print "\nBase values: " 
	# print base_values
	# print "\nBase pairwise perturbations:" 
	# print base_pairwise_perturbations

	# Preferences = List of dicts of preferences for each agent
	preferences = [{} for i in range(num_agents)]

	for preference in preferences:
		preference[frozenset()] = 0

		for singleton in singletons:
			preference[frozenset(singleton)] = float("%.2f" % (base_values[singleton] * math.trunc(random.uniform(0.5, 1.5) * 100) / 100.0))

		# all_prefs = list of all possible combinations upto team_size
		all_prefs = []

		for i in range(2, team_size + 1):
			for comb in list(itertools.combinations(singletons, i)):
				all_prefs.append(comb)

		# print "\nAll prefs:"
		# print all_prefs

		local_perturbs = {}

		for perturbation in base_pairwise_perturbations:
			local_perturbs[perturbation] = float("%.2f" % (base_pairwise_perturbations[perturbation] * math.trunc(random.uniform(0.5, 1.5) * 100) / 100.0))

		# print "\nLocal perturbs:"
		# print local_perturbs

		for pref in all_prefs:
			poss_perturbs = []

			for comb in list(itertools.combinations(pref, 2)):
				poss_perturbs.append(frozenset(comb))

			value = sum([preference[frozenset(i)] for i in pref])

			for perturb in poss_perturbs:
				value += local_perturbs[perturb]

			preference[frozenset(pref)] = value

	# print "\nPreferences:"
	return preferences

# print generate_preferences(['A', 'B', 'C', 'D', 'E', 'F'], 2, 3)