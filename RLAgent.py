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

rl_state_size = 41
bsize = 256
batch_size_var = 128000
epoc_count = 10
verbose_val = 1
adam = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
rmsprop = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)

buy_nn = Sequential()
buy_nn.add(Dense(128, input_dim=state_size))
buy_nn.add(Activation('relu'))
buy_nn.add(Dense(2))
buy_nn.add(Activation('linear'))
buy_nn.compile(optimizer=adam, loss='mse')

buy_true = 0
buy_false = 0
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

class AgentTwo:
    def __init__(self, id):
        self.id = id
        self.prev_state = None

    def getBSMTDecision(self, state):
        return False

    def respondTrade(self, state):
        return False

    def buyProperty(self, state):
#        global buy_false, buy_true
#        state = getRLState(state)
#        if self.prev_state is not None:
#            self.trainData(,,,)
#        self.prev_state = state
#        global epsilon
#        if random.random() < epsilon:
#            NNout = random.randint(0,1)
#        else:
#            NNout = np.argmax(buy_nn.predict(state))
#        self.prev_choice = NNout
#        if NNout == 1:
#            buy_true += 1
            return True
#        else:
#            buy_false += 1
#            return False

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
        group_id = state[PLAYER_POSITION_INDEX][id]
        return group_id

    def getRLState(self, state):
        count = [0,0]
        value = [0,0]
        rl_state = np.zeros((1,rl_state_size))
        value[self.id-1] = state[PLAYER_CASH_INDEX][self.id-1] - board[PLAYER_POSITION_INDEX[self.id-1]]["build_cost"]
        value[2-self.id] = state[PLAYER_CASH_INDEX][2-self.id]
        for i in range(20):
            if value[self.id-1] >= i*50 and val[self.id-1] < (i+1)*50:
                rl_state[0, 22*(self.id-1)+i+1] = 1
                break
        if value[self.id-1] >= 20*50:
            rl_state[0,22*(self.id-1)+21] = 1
        if value[self.id-1] < 0:
            rl_state[0,22*(self.id-1)] = 1
        for i in range(20):
            if value[2-self.id] >= i*50 and val[2-self.id] < (i+1)*50:
                rl_state[0, 22*(2-self.id)+i+1] = 1
                break
        if value[2-self.id] >= 20*50:
            rl_state[0,22*(2-self.id)+21] = 1
        if value[2-self.id] < 0:
            rl_state[0,22*(2-self.id)] = 1
        rl_state[0,44] = getPropertyCount(self.id-1, state)/10
        rl_state[0,45] = getPropertyCount(2-self.id, state)/10
        rl_state[0,46 + getGroupId(self.id, state)] = 1
        for i in range(10):
            for j in len(groups[i]):
                property_pos = groups[i][j]
                if state[PROPERTY_STATUS_INDEX][property_pos] > 0:
                    count[0] += 1
                elif state[PROPERTY_STATUS_INDEX][property_pos] < 0:
                    count[1] += 1
            rl_state[0, 56 + 10*(self.id-1) + i] = count[self.id-1]/len(groups[i])
            rl_state[0, 56 + 10*(2-self.id) + i] = count[2-self.id]/len(groups[i])
        return rl_state

    def trainData(self, beforeState, afterState, reward, choice):
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
        curQ = buy_nn.predict(dbstate.reshape(bsize, rl_state_size), batch_size = batch_size_var)
        newQ = buy_nn.predict(dastate.reshape(bsize, rl_state_size), batch_size = batch_size_var)
        maxQ = newQ.max(1)
        y = np.zeros((bsize, 2))
        y[:] = curQ[:]
        for i in range(bsize):
            if dataReward[i] == 0:
                y[i][dataChoice[i]] = dataReward[i] + gamma*maxQ[i]
            else:
                y[i][dataChoice[i]] = dataReward[i]
        buy_nn.fit(dbstate.reshape(bsize, state_size), y, batch_size = batch_size_var, epochs = epoc_count, verbose = verbose_val)


        #clearing the buffers
        dataBefore = []
        dataAfter = []
        dataChoice = []
        dataReward = []