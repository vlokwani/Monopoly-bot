from adjudicator import Adjudicator
from Agent import AgentOne
from Agent2 import AgentTwo

agentOne = AgentOne(1)
agentTwo = AgentTwo(2)
board = Adjudicator()
[winner, final_state] = board.runGame(agentOne=agentOne, agentTwo=agentTwo)

# print("Printing final state returned by run game: ")
# print(final_state)

final_state = board.state

print("\n\n\n\n")

print(winner)

