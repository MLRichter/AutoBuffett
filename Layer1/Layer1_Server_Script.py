__author__ = 'matsrichter'

import learnerV2a as rll
import Sender_Receiver as sr
import time as time

# sender / receiver init
sender_receiver = sr.Sender_Receiver()

#time = t.time()
instruction_dict = ""
while(instruction_dict == ""):
    instruction_dict = sender_receiver.receive()
    if instruction_dict == "":
        time.sleep(1)

#init learner parameter
learn = instruction_dict['learn']
adaption = instruction_dict['adaption']
transCost = instruction_dict['transactionCost']
weightDecay = instruction_dict['weightDecay']
m = instruction_dict['m']
#init initial prices
price2 = instruction_dict['long_price']
price1 = 0

#init the learner
learner = rll.Learner(learn,adaption,transCost,weightDecay,m)
instruction_dict['decision'] = 0
#send information to layer2 for initialization (the first decision is ignored anyway)
sender_receiver.send(instruction_dict)

while(True):
    #receive new message
    instruction_dict = sender_receiver.receive()
    if instruction_dict == "":
        time.sleep(1)
        continue
    #update price
    price1 = price2
    price2 = instruction_dict['long_price']
    #update parameters
    learner.learn = instruction_dict['learn']
    learner.adaption = instruction_dict['adaption']
    learner.transCost = instruction_dict['transactionCost']
    learner.weightDecay = instruction_dict['weightDecay']
    #make decision
    instruction_dict['decision'] = learner.predict(price1,price2)
    #send decision
    sender_receiver.send(instruction_dict)