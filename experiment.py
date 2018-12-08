import sys, os
import csv
import progressbar

sys.path.append(os.path.abspath(os.path.join(os.path.dirname('__file__'), 'Monopoly')))

from adjudicator import Adjudicator
from Agent_fixed_policy2 import AgentOne as fPolicyAgent2
from Agent import AgentOne as fPolicyAgent1
from Agent0 import AgentZero
from RLAgent import AgentRL


# agentOne = AgentZero(1)


# fpolicyAgent1 = fPolicyAgent1(1)
# fpolicyAgent2 = fPolicyAgent2(2)
# agentZero = AgentZero(2)
# board = Adjudicator()
# results = []
# for i in range(100):
#     [winner, final_state] = board.runGame(agentOne=agentRL, agentTwo=fpolicyAgent2)
#     results.append(winner)
#     count_1 = 0
#     count_2 = 0
#     for i in results:
#         if(i==1):
#             count_1+=1
#         else:
#             count_2+=1
#     with open('results-100.csv', 'w') as myfile:
#         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#         wr.writerow(results)
#     with open('results-summary.csv', 'w') as myfile:
#         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#         wr.writerow([count_1, count_2])

# # print("Printing final state returned by run game: ")
# # print(final_state)

# final_state = board.state

# ownership = {
#     0: [],
#     1: [],
#     -1: []
# }
# for i in range(len(final_state[1])):
#     owner = final_state[1][i]
#     if owner:
#         owner /= abs(owner)
#     ownership[owner].append(i)
# # fpolicyAgent1 = fPolicyAgent1(1)
# # fpolicyAgent2 = fPolicyAgent2(2)

headers = "GAME,PLAYER,PLAYER_TURN,PROPERTY_STATUS,PLAYER_POSITION,PLAYER_CASH,PHASE_NUMBER,PAYLOAD_DATA,DEBT"

def write_headers():
    with open('train.tsv', 'w') as f:
        f.write("\t".join(headers.split(',')))
        f.write("\n")


board = Adjudicator()
final_results = [0, 0]
write_headers()
for i in progressbar.progressbar(range(1000)):
    results = []
    agentRL = AgentRL(1, i)
    agentZero = AgentZero(2, i)
    fpolicyAgent1 = fPolicyAgent1(2, i)
    fpolicyAgent2 = fPolicyAgent2(2, i)
    [winner, final_state] = board.runGame(agentOne=agentRL, agentTwo=fpolicyAgent1)
    results.append(winner)

    # print("Printing final state returned by run game: ")
    # print(final_state)

    final_state = board.state

    ownership = {
        0: [],
        1: [],
        -1: []
    }
    # for i in range(len(final_state[1])):
    #     owner = final_state[1][i]
    #     if owner:
    #         owner /= abs(owner)
    #     ownership[owner].append(i)

    # print(ownership)
    
    count1, count2 = 0, 0
    for i in results:
        if i == 1:
            count1 += 1
        if i == 2:
            count2 += 1

    # with open('results-100.csv', 'w') as myfile:
    #     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #     wr.writerow(results)
    # with open('results-summary.csv', 'w') as myfile:
    #     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #     wr.writerow([count1, count2])

    # print( count1/len(results), count2/len(results))
    final_results[0] += count1/len(results)
    final_results[1] += count2/len(results)
    # print(winner)

print(final_results[0]/10, final_results[1]/10)
