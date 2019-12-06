from rml import rml
from rsd import rsd
from snake_draft import snake_draft
from gen_prefs import generate_preferences
import matplotlib.pyplot as plt
import numpy as np

def find_allocations(num_agents, team_size, RML_max_bundle_size, RML_budget):
	# num_agents = 3
	# team_size = 5
	# RML_max_bundle_size = 3
	# RML_budget = 10000
	players = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

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

	return rmlBidderVals, snake_draft_values, rsd_values

	# print "\nRML Allocation:"
	# print rmlResults

	# print "\nRML Values:"
	# print rmlBidderVals

	# print "\nSnake Draft Allocation:"
	# print snake_draft_alloc

	# print "\nSnake Draft Values:"
	# print snake_draft_values

	# print "\nRSD Allocation:"
	# print rsd_alloc

	# print "\nRSD Values:"
	# print rsd_values

to_plot_rml = []
to_plot_snake = []
to_plot_rsd = []

# To overwrite file, change to "w". Currently appends 
f=open("RML.txt", "a+")

# Comment this out after the first run.
f.write("Bundle size = 1\n")

for bundle_size in range(1, 2):
	print "\nBUNDLE SIZE:"
	print bundle_size

	rml_val_aggregate = []
	snake_val_aggregate = []
	rsd_val_aggregate = []

	for i in range(10):
		print "Iteration #:"
		print i + 1
		print "\n"
		[rmlv, snakev, rsdv] = find_allocations(3, 5, bundle_size, 10000)
		rml_val_aggregate.append(sum(rmlv))
		snake_val_aggregate.append(sum(snakev))
		rsd_val_aggregate.append(sum(rsdv))
	

	rml_mean = np.mean(rml_val_aggregate)
	rml_sd = np.std(rml_val_aggregate)
	f.write(str(rml_mean) + "\n")
	# f.write("RML Stdev: " + str(rml_sd) + "\n")
	print "RML Mean:"
	print rml_mean
	print "\nRML Stdev:"
	print rml_sd

	snake_mean = np.mean(snake_val_aggregate)
	snake_sd = np.std(snake_val_aggregate)
	# f.write("Snake Mean: " + str(snake_mean) + "\n")
	# f.write("Snake Stdev: " + str(snake_sd) + "\n")
	print "\nSnake Mean:"
	print snake_mean
	print "\nSnake Stdev:"
	print snake_sd

	rsd_mean = np.mean(rsd_val_aggregate)
	rsd_sd = np.std(rsd_val_aggregate)
	# f.write("RSD Mean: " + str(rsd_mean) + "\n")
	# f.write("RSD Stdev: " + str(rsd_sd) + "\n\n")
	print "\nRSD Mean:"
	print rsd_mean
	print "\nRSD Stdev:"
	print rsd_sd

	to_plot_rml.append(rml_mean)
	to_plot_snake.append(snake_mean)
	to_plot_rsd.append(rsd_mean)

print to_plot_rml
print to_plot_snake
print to_plot_rsd

plt.plot(range(1, 6), to_plot_rml, 'r--')
plt.plot(range(1, 6), to_plot_snake, 'bs')
plt.plot(range(1, 6), to_plot_rsd, 'g^')
plt.show()