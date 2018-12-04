
PLAYER_TURN_INDEX = 0
PROPERTY_STATUS_INDEX = 1
PLAYER_POSITION_INDEX = 2
PLAYER_CASH_INDEX = 3
PHASE_NUMBER_INDEX = 4
PHASE_PAYLOAD_INDEX = 5
DEBT_INDEX = 6


class AgentTwo:
    def __init__(self, id):
        self.id = id

    def getBSMTDecision(self, state):
        return False

    def respondTrade(self, state):
        return False

    def buyProperty(self, state):
        return True

    def auctionProperty(self, state):
        return 0

    def jailDecision(self, state):
        return "R",

    def receiveState(self, state):
        with open('agent2.log', 'a') as f:
            f.write(str(state) + "\n") 