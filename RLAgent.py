import csv
import math
import random
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import RMSprop
import keras
import numpy as np
import time
from constants import board

rl_state_size = 76
choice_options = 1
bsize = 256
batch_size_var = 128000
epoc_count = 10
verbose_val = 1
adam = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
rmsprop = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)

task_nn = Sequential()
task_nn.add(Dense(128, input_dim=rl_state_size))
task_nn.add(Activation('relu'))
task_nn.add(Dense(2))
task_nn.add(Activation('linear'))
task_nn.compile(optimizer=adam, loss='mse')

buy_true = 0
buy_false = 0
res_trade_false = 0
res_trade_true = 0
dataBefore = []
dataAfter = []
dataChoice = []
dataReward = []
epsilon = 0.1

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

groups = [[1,3], [6,8,9], [11,13,14], [16,18,19], [12,28], [21,23,24], [26,27,29], [31,32,34], [37,39], [5,15,25,35]]
groupId = [0,1,0,1,0,10,2,0,2,2,0,3,5,3,3,10,4,0,4,4,0,6,0,6,6,10,7,7,5,7,0,8,8,0,8,10,0,9,0,9]

class AgentRL:
    def __init__(self, id):
        self.id = id
        self.prev_state = None

    def getBSMTDecision(self, state):
        return False

    def respondTrade(self, state):
        global res_trade_false, res_trade_true, choice_options
        cash_offer = state[PHASE_PAYLOAD_INDEX][0]
        properties_offer = state[PHASE_PAYLOAD_INDEX][1]
        cash_request = state[PHASE_PAYLOAD_INDEX][2]
        properties_request = state[PHASE_PAYLOAD_INDEX][3]
        copy_state = self.copyState(state)
        copy_state[PLAYER_CASH_INDEX][self.id - 1] = copy_state[PLAYER_CASH_INDEX][self.id - 1] + (cash_offer - cash_request)
        copy_state[PLAYER_CASH_INDEX][2 - self.id] = copy_state[PLAYER_CASH_INDEX][2 - self.id] + (cash_request - cash_offer)
        for i in properties_offer:
            copy_state[PROPERTY_STATUS_INDEX][i] *= -1
        for i in properties_request:
            copy_state[PROPERTY_STATUS_INDEX][i] *= -1
        rl_state = self.getRLState(copy_state)
        choice_options = 2
        if self.prev_state is not None:
            self.trainData(self.prev_state[0], rl_state[0], 0, self.prev_choice, choice_options)
        self.prev_state = rl_state
        global epsilon
        if random.random() < epsilon:
            NNout = random.randint(0,1)
        elif (cash_offer - cash_request) < 0:
            NNout = 0
        else:
            NNout = np.argmax(task_nn.predict(rl_state))
        self.prev_choice = NNout
        if NNout == 1:
            res_trade_true += 1
            return True
        else:
            res_trade_false += 1
        return False

    def buyProperty(self, state):
#        global buy_false, buy_true, choice_options
#        rl_state = self.getRLState(state)
#        value = state[PLAYER_CASH_INDEX][self.id-1] - board[PLAYER_POSITION_INDEX[self.id-1]]["build_cost"]
#        if value[self.id-1] < 0:
#            rl_state[0,22*(self.id-1)] = 1
#            for i in range(20):
#                rl_state[0,22*(self.id-1)+i+1] = 0
#        elif value[self.id-1] >= 20*50:
#            rl_state[0,22*(self.id-1)+21] = 1
#        else for i in range(20):
#            if value[self.id-1] >= i*50 and value[self.id-1] < (i+1)*50:
#                rl_state[0, 22*(self.id-1)+i+1] = 1
#            else:
#                rl_state[0, 22*(self.id-1)+i+1] = 0
#        choice_options = 2
#        if self.prev_state is not None:
#            self.trainData(self.prev_state[0], rl_state[0], 0, self.prev_choice, choice_options)
#        self.prev_state = rl_state
#        global epsilon
#        if random.random() < epsilon:
#            NNout = random.randint(0,1)
#        else:
#            NNout = np.argmax(task_nn.predict(rl_state))
#        self.prev_choice = NNout
#        if NNout == 1:
#            buy_true += 1
            return True
#        else:
#            buy_false += 1
#            return False

    def auctionProperty(self, state):
#        global choice_options, epsilon
#        rl_state = self.getRLState(state)
#        if self.prev_state is not None:
#            choice_options = 350
#            self.trainData(self.prev_state[0], rl_state[0], 0, self.prev_choice, choice_options)
#        self.prev_state = rl_state
#        if random.random() < epsilon:
#            property_pos = state[PLAYER_POSITION_INDEX][self.id-1]
#            NNout = random.randint(0, (board[property_pos]["price"])+1)
#        else:
#            NNout = np.argmax(task_nn.predict(rl_state))
#        self.prev_choice = NNout
#        return NNout
        return 0

    def jailDecision(self, state):
#        global choice_options, epsilon
#        if [state[PROPERTY_STATUS_INDEX][40] == 1]:
#            choice = ["R", "P", ["C", 40]
#        elif [state[PROPERTY_STATUS_INDEX][41] == 1]:
#            choice = ["R", "P", ["C", 41]
#        else:
#            choice = ["R", "P"]
#        if random.random() < epsilon:
#            NNout = random.randint(0,len(choice))
#            if (NNout == 1) and (state[PLAYER_CASH_INDEX][self.id-1] >= 50):
#                copy_state = self.copyState(state)
#                copy_state[PLAYER_CASH_INDEX][self.id-1] -= 50
#                rl_state = self.getRLState(copy_state)
#            else:
#                rl_state = self.getRLState(state)
#        else:
#            NNout = np.argmax(task_nn.predict(rl_state))
#        if NNout >= len(choice):
#            return "R"
#        if self.prev_state is not None:
#            choice_options = 3
#            self.trainData(self.prev_state[0], rl_state[0], 0, self.prev_choice, choice_options)
#        self.prev_state = rl_state
#        self.prev_choice = NNout
#        return choice[NNout]
        return "R"

    def receiveState(self, state):
        with open('train.tsv', 'a') as f:
            f.write(str(self.id) + "\t")
            for index in state_indexes:
                f.write(str(state[index]) + "\t")
            f.write("\n")

    def copyState(self, state):
        copy_state = []
        for i in range(0,len(state)):
            if type(state[i]) == type(0):
                copy_state.append(state[i])
            else :
                temp = []
                for j in state[i]:
                    temp.append(j)
                copy_state.append(temp)
        return copy_state

    def getPropertyCount(self, id, state):
        count = [0,0]
        for i in range(40):
            property_i = state[PROPERTY_STATUS_INDEX][i]
            if ((board[i]["class"] == "Street") or (board[i]["class"] == "Railroad") or (board[i]["class"] == "Utility")):
                if property_i > 0:
                    count[0] += 1
                elif property_i < 0:
                    count[1] += 1
        return count[id]

    def getGroupId(self, id, state):
        player_pos = state[PLAYER_POSITION_INDEX][id-1]
        group_id = groupId[player_pos]
        return group_id

    def getRLState(self, state):
        count = [0,0]
        value = [0,0]
        rl_state = np.zeros((1,rl_state_size))
        value[self.id-1] = state[PLAYER_CASH_INDEX][self.id-1]
        value[2-self.id] = state[PLAYER_CASH_INDEX][2-self.id]
        for i in range(20):
            if value[self.id-1] >= i*50 and value[self.id-1] < (i+1)*50:
                rl_state[0, 22*(self.id-1)+i+1] = 1
                break
        if value[self.id-1] >= 20*50:
            rl_state[0,22*(self.id-1)+21] = 1
        if value[self.id-1] < 0:
            rl_state[0,22*(self.id-1)] = 1
        for i in range(20):
            if value[2-self.id] >= i*50 and value[2-self.id] < (i+1)*50:
                rl_state[0, 22*(2-self.id)+i+1] = 1
                break
        if value[2-self.id] >= 20*50:
            rl_state[0,22*(2-self.id)+21] = 1
        if value[2-self.id] < 0:
            rl_state[0,22*(2-self.id)] = 1
        rl_state[0,44] = self.getPropertyCount(self.id-1, state)/10
        rl_state[0,45] = self.getPropertyCount(2-self.id, state)/10
        rl_state[0,46 + self.getGroupId(self.id, state)] = 1
        for i in range(10):
            for j in range(len(groups[i])):
                property_pos = groups[i][j]
                if state[PROPERTY_STATUS_INDEX][property_pos] > 0:
                    count[0] += 1
                elif state[PROPERTY_STATUS_INDEX][property_pos] < 0:
                    count[1] += 1
            rl_state[0, 56 + 10*(self.id-1) + i] = count[self.id-1]/len(groups[i])
            rl_state[0, 56 + 10*(2-self.id) + i] = count[2-self.id]/len(groups[i])
        return rl_state

    def trainData(self, beforeState, afterState, reward, choice, choice_size):
        global dataBefore, dataAfter, dataReward, dataChoice
        dataBefore.append(beforeState)
        dataAfter.append(afterState)
        dataReward.append(reward)
        dataChoice.append(choice)
        if(len(dataChoice) < bsize):
            return
        gamma = 0.99
        dbstate = np.asarray(dataBefore)
        dastate = np.asarray(dataAfter)
        curQ = task_nn.predict(dbstate.reshape(bsize, rl_state_size), batch_size = batch_size_var)
        newQ = task_nn.predict(dastate.reshape(bsize, rl_state_size), batch_size = batch_size_var)
        maxQ = newQ.max(1)
        y = np.zeros((bsize, choice_size))
        y[:] = curQ[:]
        for i in range(bsize):
            if dataReward[i] == 0:
                y[i][dataChoice[i]] = dataReward[i] + gamma*maxQ[i]
            else:
                y[i][dataChoice[i]] = dataReward[i]
        task_nn.fit(dbstate.reshape(bsize, rl_state_size), y, batch_size = batch_size_var, epochs = epoc_count, verbose = verbose_val)


        #clearing the buffers
        dataBefore = []
        dataAfter = []
        dataChoice = []
        dataReward = []
