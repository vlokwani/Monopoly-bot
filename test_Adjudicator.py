import adjudicator as adj

TURN_NO = 0
STATUS_OF_PROPERTY = 1
POSITION_OF_PLAYER = 2
PLAYERS_MONEY = 3
CURRENT_PHASE = 4
ADDITIONAL_PHASE_INFORMATION = 5
PAST_STATES = 6


def compare_states(state_1, state_2):
    for i in range(len(state_1)):
        if state_1[i] != state_2[i]:
            return False
	return True


def testcase_buildHouse(Adjudicator):
	class Agent_1:
		def __init__(self, id):
			self.id = id

		def getBMSTDecision(self, state):
			if (state[STATUS_OF_PROPERTY][37] == 1) and (state[STATUS_OF_PROPERTY][39] == 1):
				return ("B", [(37, 1), (39, 1)])
			else:
				return None

		def buyProperty(self, state):
			if (state[POSITION_OF_PLAYER][1] == 37) or (state[POSITION_OF_PLAYER][1] == 39):
				return True
			else:
				return False

		def auctionProperty(self, state):
			return False

		def receiveState(self, state):
			pass

		def jailDecision(self, state):
			return ("R")

		def respondTrade(self, state):
			return False
		
	class Agent_2:
		def __init__(self, id):
			self.id = id

		def getBMSTDecision(self, state):
			pass
		
		def buyProperty(self, state):
			return False
		
		def auctionProperty(self, state):
			return 0
		
		def respondTrade(self, state):
			return False
			
		def jailDecision(self, state):
			return ("R")

		def receiveState(self, state):
			pass

	adjudicator = Adjudicator()
	winner, output_state = adjudicator.runGame(Agent_1(1), Agent_2(2), [[5, 6], [1, 5], [5, 5], [1, 1], [6, 5], [6, 1], [1, 4], [2, 2], [1, 1]], None, None)
	expected_state = [9, [0]*37 + [2, 0, 2, 0, 0], [39, 19], [1500 -350 -400 -200 -200, 1500], 0, [-1]*4, []]
	result = compare_states(output_state, expected_state)
	return result


def testcase_sellHouse_payRent(Adjudicator):
	class Agent_1:
		def __init__(self, id):
			self.id = id

		def getBMSTDecision(self, state):
			if (state[STATUS_OF_PROPERTY][37] == 2) and (state[STATUS_OF_PROPERTY][39] == 2):
				return ("S", [(37, 1)])
			else if (state[STATUS_OF_PROPERTY][37] == 1) and (state[STATUS_OF_PROPERTY][39] == 1):
				return ("B", [(37, 1), (39, 1)])
			else:
				return None

		def buyProperty(self, state):
			if (state[POSITION_OF_PLAYER][1] == 37) or (state[POSITION_OF_PLAYER][1] == 39):
				return True
			else:
				return False

		def auctionProperty(self, state):
			return False

		def receiveState(self, state):
			pass

		def jailDecision(self, state):
			return ("R")

		def respondTrade(self, state):
			return False

	class Agent_2:
		def __init__(self, id):
			self.id = id

		def getBMSTDecision(self, state):
			pass
		
		def buyProperty(self, state):
			return False
		
		def auctionProperty(self, state):
			return 0
		
		def respondTrade(self, state):
			return False
			
		def jailDecision(self, state):
			return ("R")

		def receiveState(self, state):
			pass

	adjudicator = Adjudicator()
	winner, output_state = adjudicator.runGame(Agent_1(1), Agent_2(2), [[5, 6], [1, 5], [5, 5], [1, 1], [6, 5], [6, 1], [1, 4], [2, 2], [1, 1], 
		[1,1], [1,1], [1,1], [4, 6], [1,1], [5, 5], [5,5], [6, 5], [1,3], [1, 4]], None, None)
	expected_state = [19, [0]*37 + [1, 0, 2, 0, 0], [37, 39], [1500 -350 -400 -200 -200 +200 +100, 1500 -50], 0, [-1]*4, []]
	result = compare_states(output_state, expected_state)
	return result

def testcase_sellHouse_mortgageOne(Adjudicator):
	class Agent_1:
		def __init__(self, id):
			self.id = id

		def getBMSTDecision(self, state):
			if (state[STATUS_OF_PROPERTY][37] == 2) and (state[STATUS_OF_PROPERTY][39] == 2):
				return ("S", [(37, 1), (39, 1)])
			else if (state[STATUS_OF_PROPERTY][37] == 1) and (state[STATUS_OF_PROPERTY][39] == 1 and state[PLAYERS_MONEY][1] == 1500):
				return ("B", [(37, 1), (39, 1)])
			else if (state[STATUS_OF_PROPERTY][37] == 1) and (state[STATUS_OF_PROPERTY][39] == 1):
				return ("M", [37])
			else:
				return None

		def buyProperty(self, state):
			if (state[POSITION_OF_PLAYER][1] == 37) or (state[POSITION_OF_PLAYER][1] == 39):
				return True
			else:
				return False

		def auctionProperty(self, state):
			return False

		def receiveState(self, state):
			pass

		def jailDecision(self, state):
			return ("R")

		def respondTrade(self, state):
			return False

	class Agent_2:
		def __init__(self, id):
			self.id = id

		def getBMSTDecision(self, state):
			return None
		
		def buyProperty(self, state):
			return False
		
		def auctionProperty(self, state):
			return 0
		
		def respondTrade(self, state):
			return False
			
		def jailDecision(self, state):
			return ("R")

		def receiveState(self, state):
			pass

	adjudicator = Adjudicator()
	winner, output_state = adjudicator.runGame(Agent_1(1), Agent_2(2), [[5, 6], [1, 5], [5, 5], [1, 1], [6, 5], [6, 1], [1, 4], [2, 2], [1, 1], 
		[1,1], [1,1], [1,1], [4, 6], [1,1], [5, 5], [5,5], [6, 5], [1,3], [1, 4]], None, None)
	expected_state = [19, [0]*37 + [0, 0, 1, 0, 0], [37, 39], [1500 -350 -400 -200 -200 +200 +100 +100 +175, 1500 -50], 0, [-1]*4, []]
	result = compare_states(output_state, expected_state)
	return result

if (testcase_buildHouse(adj.Adjudicator)):
	print("Building a house - PASSED\n")
else:
	print("Building a house - FAILED\n")

if (testcase_sellHouse_payRent(adj.Adjudicator));
	print("Selling a house and Paying the rent - PASSED\n")
else:
	print("Selling a house and Paying the rent - FAILED\n")

if (testcase_sellHouse_mortgageOne(adj.Adjudicator)):
	print("Selling a house and Mortgaging a property - PASSED\n")
else:
	print("Selling a house and Mortgaging a property - FAILED\n")