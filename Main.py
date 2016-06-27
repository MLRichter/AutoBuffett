__author__ = 'matsrichter'
import LayerWrappers.Layer1_Test_Object as l1
import LayerWrappers.Layer2_Test_Object as l2
import LayerWrappers.Layer3_Test_Object as l3
import LayerWrappers.Communicator_Test as com
import random as r
import Layer3
import time as time

def init_instructionDict():
    instruction_dict = dict()



    #initialize the instruction_dict and layer 1 params
    user_input = Layer3.UI.introduction()
    instruction_dict['capital'] = user_input['capital']
    instruction_dict['account_val'] = user_input['capital']
    instruction_dict['anti_risk'] = user_input['anti_risk']
    instruction_dict['symbol'] = user_input['symbol']

    #DEBUG
    instruction_dict['DEBUG'] = user_input['DEBUG']
    instruction_dict['lever'] = user_input['lever']
    instruction_dict['dummy_reader'] = user_input['dummy_reader']
    instruction_dict['AdaBoost'] = user_input['AdaBoost']
    instruction_dict['learner'] = user_input['learner']

    #instruction for layer 2
    instruction_dict['max_draw_down'] = user_input['capital'] * 1.00
    #risk aversion is divided by 2, to avoid a high initial trading thesholds and therefore trading block by this parameter
    instruction_dict['risk_aversion'] = 0.5
    instruction_dict['stoploss'] = 50

    #instruction for layer 1
    instruction_dict['learn'] = 0.65
    instruction_dict['adaption'] = 0.9
    instruction_dict['transactionCost'] = 0.001
    instruction_dict['weightDecay'] = 1
    instruction_dict['m'] = user_input['m']
    instruction_dict['account_val'] = instruction_dict['capital']
    instruction_dict['long_price'] = 0
    instruction_dict['short_price'] = 0
    return instruction_dict

instructionDict = init_instructionDict()
layer3 = l3.Layer3(instructionDict)
layer2 = l2.Layer2(instructionDict)
layer1 = l1.Layer1(instructionDict)
communicator = com.Sender_Receiver(layer1,layer2,layer3)
layer1.adCom(communicator)
layer2.adCom(communicator)
layer3.adCom(communicator)

while(True):
    layer3.call(instructionDict)
    if('ERROR' in instructionDict):
        print(instructionDict['ERROR'])
        break