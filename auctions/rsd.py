import random

# allPrefs = list of lists of ints of each bidder's preference ordering 
# over all players, identified by unique IDs 
# team_size = integer of the number of players on a given team

def rsd(allPrefs, team_size):
    bidders = list(range(len(allPrefs)))
    random.shuffle(bidders)

    # chosen = list of player IDs that have already been chosen
    chosen = []
    # allocated = list of lists of each bidder's allocated players
    allocated = [[] for i in range(len(allPrefs))]
    # lastChosenIndex = index in preference ordering before which all are chosen
    lastChosenIndex = {key : 0 for key in range(len(allPrefs))}

    for round in range(team_size):
        for bidder in bidders:
            bidderPrefs = allPrefs[bidder]
            i = lastChosenIndex[bidder]
            while bidderPrefs[i] in chosen:
                i += 1
            lastChosenIndex[bidder] = i
            allocated[bidder].append(bidderPrefs[i])
            chosen.append(bidderPrefs[i])
    return allocated

# test = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], 
# [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
# [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
# [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
# [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]]

# Players: 0 - 20
# Bidders: 0 - 5
# Num rounds: 3
# print(rsd(test, 3))