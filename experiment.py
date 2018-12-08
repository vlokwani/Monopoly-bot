import sys, os
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname('__file__'), 'Monopoly')))

from adjudicator import Adjudicator
from Agent_fixed_policy2 import AgentOne as fPolicyAgent2
from Agent import AgentOne as fPolicyAgent1
from Agent0 import AgentZero
from RLAgent import AgentRL


# agentOne = AgentZero(1)
agentRL = AgentRL(2)

fpolicyAgent1 = fPolicyAgent1(1)
fpolicyAgent2 = fPolicyAgent2(2)
agentZero = AgentZero(2)
board = Adjudicator()
results = []
for i in range(100):
    [winner, final_state] = board.runGame(agentOne=fpolicyAgent1, agentTwo=agentRL)
    results.append(winner)
    count_1 = 0
    count_2 = 0
    for i in results:
        if(i==1):
            count_1+=1
        else:
            count_2+=1
    with open('results-100.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(results)
    with open('results-summary.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([count_1, count_2])

# print("Printing final state returned by run game: ")
# print(final_state)

final_state = board.state

ownership = {
    0: [],
    1: [],
    -1: []
}
for i in range(len(final_state[1])):
    owner = final_state[1][i]
    if owner:
        owner /= abs(owner)
    ownership[owner].append(i)



print("\n\n\n\n")

print(ownership)

print("\n\n\n\n")



print(winner)
