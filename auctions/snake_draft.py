def snake_draft(preference_orders, num_rounds):
	"""
	Input: 
	* [preference_orders] List of lists. List per bidder 0, ..., n - 1 representing
	strict pref order over players 0, ..., m - 1. 
	* [num_rounds] Int. Number of times to snake.

	Output: 
	* List of lists. List per bidder 0, ..., n - 1 representing snake draft
	allocation.
	"""
	current_round = 0

	allocs = [[] for i in range(len(preference_orders))]
	allocated = {}

	while current_round < num_rounds:
		if current_round % 2 == 0:
			for i in range(len(preference_orders)):
				for j in range(len(preference_orders[i])):
					if preference_orders[i][j] not in allocated:
						allocs[i].append(preference_orders[i][j])
						allocated.add(preference_orders[i][j])
		else:
			for i in range(len(preference_orders) - 1, -1, -1):
				for j in range(len(preference_orders[i])):
					if preference_orders[i][j] not in allocated:
						allocs[i].append(preference_orders[i][j])
						allocated.add(preference_orders[i][j])
		current_round += 1

	return allocs