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

def testcase_buyProperty(Adjudicator):
	class Agent_1:
		def __init__(self, id):
			self.id = id

		def getBSMTDecision(self, state):
				return None

		def buyProperty(self, state):
				return True

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

		def getBSMTDecision(self, state):
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
	winner, output_state = adjudicator.runGame(Agent_1(1), Agent_2(2), [[1, 2]], None, None)
	expected_state = [1, [0]*3 + [1] + [0]*38, [3, 0], [1500 -60, 1500], 0, [0]*4, []]
	result = compare_states(output_state, expected_state)
	print(output_state)
	print("-------------")
	print(expected_state)
	return result

def testcase_auctionProperty(Adjudicator):
	class Agent_1:
		def __init__(self, id):
			self.id = id

		def getBSMTDecision(self, state):
				return None

		def buyProperty(self, state):
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

		def getBSMTDecision(self, state):
			pass

		def buyProperty(self, state):
			return False

		def auctionProperty(self, state):
			return 100

		def respondTrade(self, state):
			return False

		def jailDecision(self, state):
			return ("R")

		def receiveState(self, state):
			pass

	adjudicator = Adjudicator()
	winner, output_state = adjudicator.runGame(Agent_1(1), Agent_2(2), [[1, 2]], None, None)
	expected_state = [1, [0]*3 + [-1] + [0]*38, [3, 0], [1500, 1500-100], 0, [0]*4, []]
	result = compare_states(output_state, expected_state)
	print(output_state)
	print("-------------")
	print(expected_state)
	return result

def testcase_auctionSameAmount(Adjudicator):
	class Agent_1:
		def __init__(self, id):
			self.id = id

		def getBSMTDecision(self, state):
				return None

		def buyProperty(self, state):
				return False

		def auctionProperty(self, state):
			return 100

		def receiveState(self, state):
			pass

		def jailDecision(self, state):
			return ("R")

		def respondTrade(self, state):
			return False

	class Agent_2:
		def __init__(self, id):
			self.id = id

		def getBSMTDecision(self, state):
			pass

		def buyProperty(self, state):
			return False

		def auctionProperty(self, state):
			return 100

		def respondTrade(self, state):
			return False

		def jailDecision(self, state):
			return ("R")

		def receiveState(self, state):
			pass

	adjudicator = Adjudicator()
	winner, output_state = adjudicator.runGame(Agent_1(1), Agent_2(2), [[1, 2]], None, None)
	expected_state = [1, [0]*3 + [-1] + [0]*38, [3, 0], [1500, 1500-100], 0, [0]*4, []]
	result = compare_states(output_state, expected_state)
	print(output_state)
	print("-------------")
	print(expected_state)
	return result

if (testcase_buyProperty(adj.Adjudicator)):
	print("Buying a property - PASSED\n")
else:
	print("Buying a property - FAILED\n")
if (testcase_auctionProperty(adj.Adjudicator)):
	print("Auction a property - PASSED\n")
else:
	print("Auction a property - FAILED\n")
if (testcase_auctionSameAmount(adj.Adjudicator)):
	print("Auction a property with tie - PASSED\n")
else:
	print("Auction a property with tie- FAILED\n")
