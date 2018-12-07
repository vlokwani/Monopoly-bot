import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname('__file__'), 'Monopoly')))

from adjudicator import Adjudicator
from Agent import AgentOne
from Agent0 import AgentZero

agentOne = AgentOne(1)
agentTwo = AgentZero(2)
board = Adjudicator()
results = []
for i in range(100):
    [winner, final_state] = board.runGame(agentOne=agentOne, agentTwo=agentTwo)
    results.append(winner)

# print("Printing final state returned by run game: ")
# print(final_state)

final_state = board.state

print("\n\n\n\n")

print(winner)

