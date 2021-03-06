
PLAYER_TURN_INDEX = 0
PROPERTY_STATUS_INDEX = 1
PLAYER_POSITION_INDEX = 2
PLAYER_CASH_INDEX = 3
PHASE_NUMBER_INDEX = 4
PHASE_PAYLOAD_INDEX = 5
DEBT_INDEX = 6


state_indexes = [
    PLAYER_TURN_INDEX,
    PROPERTY_STATUS_INDEX,
    PLAYER_POSITION_INDEX,
    PLAYER_CASH_INDEX,
    PHASE_NUMBER_INDEX,
#    PHASE_PAYLOAD_INDEX,
    DEBT_INDEX
]

class AgentZero:
    def __init__(self, id):
        self.id = id

    def getBSMTDecision(self, state):
        return False

    def respondTrade(self, state):
        return False

    def buyProperty(self, state):
        return False

    def auctionProperty(self, state):
        return 0

    def jailDecision(self, state):
        return "R",

    def receiveState(self, state):
        with open('train.tsv', 'a') as f:
            f.write(str(self.id) + "\t")
            for index in state_indexes:
                f.write(str(state[index]) + "\t")
            f.write("\n")
