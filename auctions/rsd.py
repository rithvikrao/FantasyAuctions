import random

# allPrefs = dict of lists of ints of each bidder's preference ordering 
# over all players, identified by unique IDs 
# numRounds = integer of the number of players on a given team

def rsd(allPrefs, numRounds):
    bidders = list(range(len(allPrefs)))
    random.shuffle(bidders)

    # chosen = list of player IDs that have already been chosen
    chosen = []
    # allocated = dict of bidder : list of their allocated players by ID pairs
    allocated = {key : [] for key in range(len(allPrefs))}
    # lastChosenIndex = index in preference ordering before which all are chosen
    lastChosenIndex = {key : 0 for key in range(len(allPrefs))}

    for round in range(numRounds):
        for bidder in bidders:
            bidderPrefs = allPrefs[bidder]
            i = lastChosenIndex[bidder]
            while bidderPrefs[i] in chosen:
                i += 1
            lastChosenIndex[bidder] = i
            allocated[bidder].append(bidderPrefs[i])
            chosen.append(bidderPrefs[i])
    return allocated

test = {0: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], 
1: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
2: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
3: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
4: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]}

# Players: 0 - 20
# Bidders: 0 - 5
# Num rounds: 3
print(rsd(test, 3))