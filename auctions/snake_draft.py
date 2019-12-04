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
	allocated = set()

	while current_round < num_rounds:
		if current_round % 2 == 0:
			loop_over = range(len(preference_orders))
		else:
			loop_over = reversed(range(len(preference_orders)))

		for i in loop_over:
			for j in range(len(preference_orders[i])):
				if preference_orders[i][j] not in allocated:
					allocs[i].append(preference_orders[i][j])
					allocated.add(preference_orders[i][j])
					break

		current_round += 1

	return allocs


print(snake_draft([[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], 
			[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
			[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
			[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
			[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]], 3))