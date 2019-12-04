import random

# allPrefs = list of lists of ints of each bidder's preference ordering 
# over all players, identified by unique IDs 
# numRounds = integer of the number of players on a given team

def rsd(allPrefs, numRounds):
    random.shuffle(allPrefs)
    # chosen = list of player IDs that have already been chosen
    chosen = []
    # allocated = dict of bidder : list of their allocated players by ID pairs
    allocated = {key : [] for key in range(len(allPrefs))}
    for i in range(numRounds):
        for bidder in range(len(allPrefs)):
            bidderPrefs = allPrefs[bidder]
            i = 0
            while bidderPrefs[i] in chosen:
                i += 1
            allocated[bidder].append(bidderPrefs[i])
            chosen.append(bidderPrefs[i])
    
