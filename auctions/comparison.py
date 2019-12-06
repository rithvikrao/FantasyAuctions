from rml import rml
from rsd import rsd
from snake_draft import snake_draft
from gen_prefs import generate_preferences
import matplotlib as plt

players = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
num_agents = 3
team_size = 2

RML_max_bundle_size = 3
RML_budget = 10000

preferences = generate_preferences(players, num_agents, team_size)
rmlResults = rml(num_agents, team_size, RML_max_bundle_size, RML_budget, preferences)

rmlBidderVals = []
for bidder in range(len(rmlResults)):
    rmlBidderVals.append(preferences[bidder][rmlResults[bidder]])

singleton_values = [{} for i in range(len(preferences))]

# Loop over agents
for i in range(len(preferences)):
    # Then over singleton players
    for player in players:
        singleton_values[i][frozenset(player)] = preferences[i][frozenset(player)]

ordinal_prefs = [[] for i in range(len(preferences))]
snake_draft_values = [0 for i in range(len(preferences))]

for i in range(len(singleton_values)):
    tuples = singleton_values[i].items()
    tuples.sort(key = lambda x : -x[1])
    for (singleton, value) in tuples:
        ordinal_prefs[i].append(singleton)

snake_draft_alloc = snake_draft(ordinal_prefs, team_size)

for i in range(len(snake_draft_alloc)):
	bidder_alloc = snake_draft_alloc[i]
	combo = set() 

	for player in bidder_alloc:
		combo = combo.union(player)

	snake_draft_values[i] = preferences[i][frozenset(combo)]

rsd_alloc = rsd(ordinal_prefs, team_size)
rsd_values = [0 for i in range(len(preferences))]
for i in range(len(rsd_alloc)):
	bidder_alloc = rsd_alloc[i]
	combo_rsd = set() 
	for player in bidder_alloc:
		combo_rsd = combo_rsd.union(player)
	rsd_values[i] = preferences[i][frozenset(combo_rsd)]

print "\nRML Allocation:"
print rmlResults

print "\nRML Values:"
print rmlBidderVals

print "\nSnake Draft Allocation:"
print snake_draft_alloc

print "\nSnake Draft Values:"
print snake_draft_values

print "\nRSD Allocation:"
print rsd_alloc

print "\nRSD Values:"
print rsd_values