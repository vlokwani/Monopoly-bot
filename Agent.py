
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

headers = "PLAYER,PLAYER_TURN,PROPERTY_STATUS,PLAYER_POSITION,PLAYER_CASH,PHASE_NUMBER,DEBT"

def write_headers():
    with open('train.tsv', 'w') as f:
        f.write("\t".join(headers.split(',')))
        f.write("\n")

class AgentOne:
    def __init__(self, id):
        self.id = id
        write_headers()

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
        with open('train.tsv', 'a') as f:
            f.write(str(self.id) + "\t")
            for index in state_indexes:
                f.write(str(state[index]) + "\t")
            f.write("\n")
