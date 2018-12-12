import adjudicator
			
class Bot1:
	def __init__(self, id):
		self.id = id

    def getBMSTDecision(self, state):
        return False

    def jailDecision(self, state):
        if state[0] == 19:
            return "P",
        else:
            return "R",
	
class Bot2:
	def __init__(self, id):
		self.id = id

    def getBMSTDecision(self, state):
        return False

    def jailDecision(self, state):
            return "R",

def validate_state(state1,state2):
    for i in range(len(state1)):
        if state1[i] != state2[i]:
            return False, i
	return True

def testcase1(Adjudicator,AgentOne,AgentTwo):
	# Agent1 is in jain and has decided to pay to get out.
    # The state checks if the amount is deducted his cash in hand.
    # Also, once he has payed, is he allowed to move forward.
	
	initial_state =  [19, [0] * 42, [-1, -1], [240, 540], 4, {}]
	
	expected_output_state = [20, [0] * 42, [20, 13], [190, 540], 4, {}]

	
	no_of_turns = 1
	
	adjudicator = Adjudicator(AgentOne,AgentTwo,input_state,[(3,7),(1, 6)],no_of_turns)
	adjudicator.runGame()
	
	final_state = adjudicator.state
	
	result = validate_state(final_state,expected_output_state)
	
	if result[0]: 
        print("Test Case Cleared: Pay to get out of Jail")
	else: 
        print("Test Case Failed: Pay to get out of Jail at step {}".format(result[1]))
	
	return result

def testcase2(Adjudicator,AgentOne,AgentTwo):
	# Agent1 is in jain and chooses to roll which is a double ( condition to get out of jail). 
    # The state checks if no amount is deducted and player moves the correct number of positions.
    # from the jail square.
	
	initial_state =  [22, [0] * 42, [-1, -1], [240, 540], 4, {}]
	
	expected_output_state = [23, [0] * 42, [20, -1], [240, 540], 4, {}]

	
	no_of_turns = 1
	
	adjudicator = Adjudicator(AgentOne,AgentTwo,input_state,[(5,5), (2, 7)],no_of_turns)
	adjudicator.runGame()
	
	final_state = adjudicator.state
	
	result = validate_state(final_state,expected_output_state)
	
	if result[0]: 
        print("Test Case Cleared: Roll a double to get out of jail")
	else: 
        print("Test Case Failed: Roll a double to get out of jail at step {}".format(result[1]))
	
	return result
	

def testcase3(Adjudicator,AgentOne,AgentTwo):
	# Agent1 is in jain and chooses to roll. The dice roll is not a double  and so the player won't get out of jail
    # The state checks if no amount is deducted and player moves the correct number of positions.
    # from the jail square.
	
	initial_state =  [22, [0] * 42, [-1, -1], [240, 540], 4, {}]
	
	expected_output_state = [23, [0] * 42, [-1, -1], [240, 540], 4, {}]

	
	no_of_turns = 1
	
	adjudicator = Adjudicator(AgentOne,AgentTwo,input_state,[(3,4), (5,6)],no_of_turns)
	adjudicator.runGame()
	
	final_state = adjudicator.state
	
	result = validate_state(final_state,expected_output_state)
	
	if result[0]: 
        print("Test Case Cleared: Roll a non-double and stay in jail")
	else: 
        print("Test Case Failed: Roll a non-double and stay in jail at step {}".format(result[1]))
	
	return result
#Execution
testcase1(adjudicator.Adjudicator, Bot1, Bot2)
testcase2(adjudicator.Adjudicator, Bot1, Bot2)
testcase3(adjudicator.Adjudicator, Bot1, Bot2)