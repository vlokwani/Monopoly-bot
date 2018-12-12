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
from math import ceil

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
    PHASE_PAYLOAD_INDEX,
    DEBT_INDEX
]

def write_headers():
    with open('train.tsv', 'w') as f:
        f.write("\t".join(headers.split(',')))
        f.write("\n")
        
def getMortgagePrice(price):
    return price/2

groups = [[1,3], [6,8,9], [11,13,14], [16,18,19], [12,28], [21,23,24], [26,27,29], [31,32,34], [37,39], [5,15,25,35]]
groupId = [0,1,0,1,0,10,2,0,2,2,0,3,5,3,3,10,4,0,4,4,0,6,0,6,6,10,7,7,5,7,0,8,8,0,8,10,0,9,0,9]

street_sets = [[1,3], [6,8,9], [11,13,14], [16,18,19], [21,23,24], [26,27,29], [31,32,34], [37,39]]
railroad_set = [5, 15,25,35]
utility_set = [12,28]

class AgentRL:
    def __init__(self, id, game=None):
        self.id = id
        self.buyable_properties = []
        self.property_priority_queue = []
        for i in range(40):
            if board[i]['class'] in ['Street', 'Railroad', 'Utility']:
                self.buyable_properties.append(i)
        self.initialize()
        self.trade_count_itr = 0
        self.mortgaged_properties = []
        self.game = game
        self.prev_state=None

    def initialize(self):
        for i in range(0,40):
            if(board[i]["class"]=="Street"):
                pr = board[i]["price"]
                self.property_priority_queue.append([pr,i])
            elif(board[i]["class"]=="Railroad"):
                self.property_priority_queue.append([200,i])
            elif(board[i]["class"]=="Utility"):
                self.property_priority_queue.append([150,i])
        self.property_priority_queue = list(reversed(sorted(self.property_priority_queue)))

    def getBSMTDecision(self, state):
        bsmt = False
        position = state[PLAYER_POSITION_INDEX][self.id-1]
        threshold_cash = self.calculate_threshold_cash_futue(state)
        if position in self.buyable_properties and state[PROPERTY_STATUS_INDEX][position] == 0:
            # print("Priority Queue: {}".format(self.property_priority_queue))
            properties = self.mortgage_property_to_buy(position, state)
            if properties:
                # print("Mortgaging properties: {}".format(properties))
                bsmt = ("M", properties)
                self.mortgaged_properties.extend(properties)
                return bsmt
        elif state[PLAYER_CASH_INDEX][self.id-1] <= threshold_cash:
            # sell improvements or mortgage
            # priority 1 sell
            # priority 2 mortgage
            properties = self.mortgage_or_sell()
            if properties:
                bsmt = properties
                if bsmt[0] == 'M':
                    self.mortgaged_properties.extend(properties[1])
                return bsmt
        # elif state[PLAYER_CASH_INDEX][self.id-1] > threshold_cash + 
        properties = self.offer_trade(state)
        if properties:
            bsmt = properties

        return bsmt

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
        position = state[PLAYER_POSITION_INDEX][self.id-1]
        property_for_sale = board[position]
        price = property_for_sale['price']
        # id = 1 for player 1 and 2 for player 2
        money = state[PLAYER_CASH_INDEX][self.id-1] # liquid money
        money_left = money - price
        threshold_cash = self.calculate_threshold_cash_futue(state)

        if money_left > threshold_cash:
            return True
        else:
            return False

    def auctionProperty(self, state):
        prop = state[PHASE_PAYLOAD_INDEX][0]
        property_auction = board[prop]
        price = property_auction['price']
        # id = 1 for player 1 and 2 for player 2
        money = state[PLAYER_CASH_INDEX][self.id-1] # liquid money
        money_left = money - price
        threshold_cash = self.calculate_threshold_cash_futue(state)

        if money_left < 0:
            return 0

        p2_money = state[PLAYER_CASH_INDEX][self.id-2]
        fair_value = ceil(self.get_fair_price(prop, price))

        if money_left < threshold_cash:
            # print("Proposed_auction_value1: {} for property {}:{}".format(min(money - threshold_cash, fair_value, p2_money + 1), property_auction['name'], price))
            return min(money - threshold_cash, fair_value, p2_money + 1)
        else:
            if p2_money < price:
                # print("Proposed_auction_value2: {} for property {}:{}".format(min(p2_money + 1, fair_value), property_auction['name'], price))
                return min(p2_money + 1, fair_value)
            else:
                # print("Proposed_auction_value3: {} for property {}:{}".format(fair_value, property_auction['name'], price))
                return fair_value
        return 0

    def jailDecision(self, state):
        return "R",

    #returns cash offer, [property numbers for offer], cash requesting, [property numbers requesting]
    def offer_trade(self, state):
        if(self.trade_count_itr == 0):
            #look at the property_priority_queue and get the property I want most.
            for prop in self.property_priority_queue:
                value = prop[0]
                propId = prop[1]
                if((state[PROPERTY_STATUS_INDEX][propId] > 0 and self.id==2) or (state[PROPERTY_STATUS_INDEX][propId] < 0 and self.id==1)):
                    self.trade_count_itr+=1
                    return ["T", value*0.5, [], 0, [propId]]
        elif(self.trade_count_itr == 1):
            #look at the property_priority_queue and get the property I want most.
            for prop in self.property_priority_queue:
                value = prop[0]
                propId = prop[1]
                if((state[PROPERTY_STATUS_INDEX][propId] > 0 and self.id==2) or (state[PROPERTY_STATUS_INDEX][propId] < 0 and self.id==1)):
                    self.trade_count_itr+=1
                    return ["T", value*0.6, [], 0, [propId]]
        elif(self.trade_count_itr == 2):
            #look at the property_priority_queue and get the property I want most.
            for prop in self.property_priority_queue:
                value = prop[0]
                propId = prop[1]
                if((state[PROPERTY_STATUS_INDEX][propId] > 0 and self.id==2) or (state[PROPERTY_STATUS_INDEX][propId] < 0 and self.id==1)):
                    self.trade_count_itr+=1
                    return ["T", value*0.75, [], 0, [propId]]
        elif(self.trade_count_itr == 3):
            #look at the property_priority_queue and get money for a property I don't want.
            rev_queue = list(reversed(self.property_priority_queue))
            for prop in rev_queue:
                value = prop[0]
                propId = prop[1]
                if((state[PROPERTY_STATUS_INDEX][propId] < 0 and self.id==2) or (state[PROPERTY_STATUS_INDEX][propId] > 0 and self.id==1)):
                    self.trade_count_itr += 1
                    return ["T", 0, [propId], value*3, []]
        elif(self.trade_count_itr == 4):
            #look at the property_priority_queue and get money for a property I don't want.
            rev_queue = list(reversed(self.property_priority_queue))
            for prop in rev_queue:
                value = prop[0]
                propId = prop[1]
                if((state[PROPERTY_STATUS_INDEX][propId] < 0 and self.id==2) or (state[PROPERTY_STATUS_INDEX][propId] > 0 and self.id==1)):
                    self.trade_count_itr += 1
                    return ["T", 0, [propId], value*2, []]
        elif(self.trade_count_itr == 5):
            #look at the property_priority_queue and get money for a property I don't want.
            rev_queue = list(reversed(self.property_priority_queue))
            for prop in rev_queue:
                value = prop[0]
                propId = prop[1]
                if((state[PROPERTY_STATUS_INDEX][propId] < 0 and self.id==2) or (state[PROPERTY_STATUS_INDEX][propId] > 0 and self.id==1)):
                    self.trade_count_itr = 0
                    return ["T", 0, [propId], value*1.5, []]

        return []

    #look ahead 2-12 locations and return the max money I might have to spend
    def calculate_threshold_cash_futue(self, state):
        # if possible try and add
        if(self.id == 1):
            currentPos = state[PLAYER_POSITION_INDEX][0]
        else:
            currentPos = state[PLAYER_POSITION_INDEX][1]
        if currentPos == -1:
            currentPos = 10
        maxMoney = 0
        for j in range(2,13):
            i = (j + currentPos) % 40
            money = 0
            if((state[PROPERTY_STATUS_INDEX][i] <0 and self.id==1) or (state[PROPERTY_STATUS_INDEX][i] >0 and self.id==2)):
                #its his property
                if(board[i]["class"]=="Street"):
                    status = state[PROPERTY_STATUS_INDEX][i]
                    if(status == 1 or status == -1):
                        money = board[i]["rent"]
                    elif(status == 2 or status == -2):
                        money = board[i]["rent_house_1"]
                    elif(status == 3 or status == -3):
                        money = board[i]["rent_house_2"]
                    elif(status == 4 or status == -4):
                        money = board[i]["rent_house_3"]
                    elif(status == 5 or status == -5):
                        money = board[i]["rent_house_4"]
                    elif(status == 6 or status == -6):
                        money = board[i]["rent_hotel"]
                elif(board[i]["class"]=="Utility"):
                    countUtility = 1
                    for k in utility_set:
                        if(k!=i):
                            if((state[PROPERTY_STATUS_INDEX][k] <0 and self.id==1) or (state[PROPERTY_STATUS_INDEX][k] >0 and self.id==2)):
                                countUtility += 1
                    if(countUtility == 1):
                        money = 12*4 #max dice roll
                    else:
                        money = 12*10
                elif(board[i]["class"]=="Railroad"):
                    countRail = 1
                    for k in railroad_set:
                        if(k!=i):
                            if((state[PROPERTY_STATUS_INDEX][k] <0 and self.id==1) or (state[PROPERTY_STATUS_INDEX][k] >0 and self.id==2)):
                                countRail += 1
                    money = 25*countRail
                else:
                    money = 200
            if(money > maxMoney):
                maxMoney = money
        return maxMoney

    #return property's value if I have it now and the other agent might get in future.
    def property_value_myProperty(self, propertyIndex, state):
        #find if it's their first/second/third property after trade
        their_count = 1
        pClass = board[propertyIndex]["class"]
        if(pClass=="Street"):
            for street_set in street_sets:
                if(propertyIndex in street_set):
                    for i in street_set:
                        if(i!=propertyIndex):
                            if(state[PROPERTY_STATUS_INDEX][i] <0 and self.id == 1):
                                their_count+=1
                            elif(state[PROPERTY_STATUS_INDEX][i] >0 and self.id == 2):
                                their_count+=1
        elif(pClass=="Railroad"):
            for i in railroad_set:
                if(i != propertyIndex):
                    if(state[PROPERTY_STATUS_INDEX][i] <0 and self.id == 1):
                        their_count+=1
                    elif(state[PROPERTY_STATUS_INDEX][i] >0 and self.id == 2):
                        their_count+=1
        elif(pClass=="Utility"):
            for i in utility_set:
                if(i != propertyIndex):
                    if(state[PROPERTY_STATUS_INDEX][i] <0 and self.id == 1):
                        their_count+=1
                    elif(state[PROPERTY_STATUS_INDEX][i] >0 and self.id == 2):
                        their_count+=1
        value = self.property_value(propertyIndex, their_count)
        finalValue = value + self.property_discount(propertyIndex, their_count, value)
        return finalValue

    #return property's value if other agent has it and I am getting it.
    def property_value_hisProperty(self, propertyIndex, state):
        #find if it's my first/second/third property after trade
        my_count = 1
        pClass = board[propertyIndex]["class"]
        if(pClass=="Street"):
            for street_set in street_sets:
                if(propertyIndex in street_set):
                    for i in street_set:
                        if(i!=propertyIndex):
                            if(state[PROPERTY_STATUS_INDEX][i] <0 and self.id == 2):
                                my_count+=1
                            elif(state[PROPERTY_STATUS_INDEX][i] >0 and self.id == 1):
                                my_count+=1
        elif(pClass=="Railroad"):
            for i in railroad_set:
                if(i != propertyIndex):
                    if(state[PROPERTY_STATUS_INDEX][i] <0 and self.id == 2):
                        my_count+=1
                    elif(state[PROPERTY_STATUS_INDEX][i] >0 and self.id == 1):
                        my_count+=1
        elif(pClass=="Utility"):
            for i in utility_set:
                if(i != propertyIndex):
                    if(state[PROPERTY_STATUS_INDEX][i] <0 and self.id == 2):
                        my_count+=1
                    elif(state[PROPERTY_STATUS_INDEX][i] >0 and self.id == 1):
                        my_count+=1
        value = self.property_value(propertyIndex, my_count)
        finalValue = value + self.property_discount(propertyIndex, my_count, value)
        return finalValue

    def property_discount(self, propertyIndex, count, value):
        pClass = board[propertyIndex]["class"]
        pColor = board[propertyIndex]["monopoly"]
        #Opponent can or would be able to build houses after the deal
        if(pClass=="Street" and count==2 and (pColor=="Dark Blue" or pColor=="Light Blue")):
            return value*0.3
        elif(pClass=="Street" and count==3):
            return value*0.3
        else:
            return 0

    def property_value(self, propertyIndex, count):
        pColor = board[propertyIndex]["monopoly"]
        pClass = board[propertyIndex]["class"]
        if(count==1 and pClass=="Railroad"):
            return 200
        elif(count==1 and pClass=="Utility"):
            return 150
        elif(count==1 and pClass=="Street"):
            return board[propertyIndex]["price"]
        elif(count==2 and pClass=="Railroad"):
            return 400
        elif(count==2 and pClass=="Utility"):
            return 300
        elif(count==2 and pClass=="Street"):
            if(pColor=="Light Blue"):
                return (board[propertyIndex]["price"]*2) + 150
            else:
                return board[propertyIndex]["price"]*2
        elif(count==3 and pClass=="Railroad"):
            return 600
        elif(count==3 and pClass=="Street"):
            if(pColor=="Brown"):
                return (board[propertyIndex]["price"]*3) + 200
            elif(pColor=="Light Blue"):
                return (board[propertyIndex]["price"]*3) + 300
            elif(pColor=="Pink"):
                return (board[propertyIndex]["price"]*3) + 150
            elif(pColor=="Orange"):
                return (board[propertyIndex]["price"]*3) + 250
            elif(pColor=="Red" or pColor=="Yellow"):
                return (board[propertyIndex]["price"]*3) + 100
            elif(pColor=="Green"):
                return (board[propertyIndex]["price"]*3) - 50
        elif(count==4 and pClass=="Railroad"):
            return 800
        else:
            return -1

    def updatePropertyPriority(self, state):
        for i in range(len(self.property_priority_queue)):
            prop = self.property_priority_queue[i]
            k = prop[1]
            value = prop[0]
            if((state[PROPERTY_STATUS_INDEX][k] > 0 and self.id==1) or(state[PROPERTY_STATUS_INDEX][k] < 0 and self.id==2)):
                #I own it
                value = self.property_value_myProperty(k, state)
            elif((state[PROPERTY_STATUS_INDEX][k] > 0 and self.id==2)or(state[PROPERTY_STATUS_INDEX][k] < 0 and self.id==1)):
                #he owns it
                value = self.property_value_hisProperty(k, state)
            else:
                #bank owns it, do nothing
                value = self.property_value_hisProperty(k, state)
            prop[0] = value
        self.property_priority_queue = list(reversed(sorted(self.property_priority_queue)))


    def get_my_properties(self, pstatus):
        # return list of properties that belong to me
        # for each property in priority queue, check status from pstatus
        # pstatus is nothing but state[PROPERTY_STATUS_INDEX]
        return [prop for prop in self.property_priority_queue if pstatus[prop[1]] == -1**(self.id+1)]

    def get_property_value(self, position):
        # return the property at the current position
        current_property = [prop for prop in self.property_priority_queue if prop[1] == position]
        # for prop in self.property_priority_queue:
        #     print(prop)
        return current_property[0]

    def mortgage_property_to_buy(self, position, state):
        threshold_cash = self.calculate_threshold_cash_futue(state)
        money = state[PLAYER_CASH_INDEX][self.id - 1]
        price = board[position]['price']
        money_left = money - price

        if money_left < threshold_cash:
            my_properties = self.get_my_properties(state[PROPERTY_STATUS_INDEX])
            property_value = self.get_property_value(position)
            mortgage_sum = 0
            mortgage_list = []
            for i in range(len(my_properties) -1, -1, -1):
                if my_properties[i][0] > property_value[0]:
                    break
                elif mortgage_sum >= threshold_cash - money:
                    return mortgage_list
                else:
                    mortgage_list.append(my_properties[i][1])
                    mortgage_sum += getMortgagePrice(price)
        return []

    def mortgage_or_sell(self):
        return []

    def get_fair_price(self, prop, price):
        # price = board[prop]['price']
        for i in range(28):
            if prop == self.property_priority_queue[i][1]:
                if i < 7:
                    return 1 * price + 1
                elif i < 14:
                    return 0.5 * price
                elif i < 21:
                    return 0.2 * price
                elif i < 28:
                    return 0.1 * price

    def receiveState(self, state):
        if self.game:
            with open('train.tsv', 'a') as f:
                f.write(str(self.game) +  "\t")
                f.write(str(self.id) + "\t")
                for index in state_indexes:
                    f.write(str(state[index]) + "\t")
                f.write("\n")
        self.updatePropertyPriority(state)

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
