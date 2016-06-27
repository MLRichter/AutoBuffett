from Instruction_dict import Instruction_dict
__author__ = 'matsrichter'

import Optimization_System as os
import UI
import FX_Reader as fxr
import Sender_Receiver as sr
import time as time

user_input = UI.introduction()
tstep = 0

#instruction_dict = dict()
#initialize the instruction_dict and layer 1 params
#user_input = UI.introduction()
Instruction_dict.values['capital'] = user_input['capital']
Instruction_dict.values['account_val'] = user_input['capital']
Instruction_dict.values['anti_risk'] = user_input['anti_risk']
Instruction_dict.values['symbol'] = user_input['symbol']

#DEBUG
Instruction_dict.values['DEBUG'] = user_input['DEBUG']
Instruction_dict.values['lever'] = user_input['lever']
Instruction_dict.values['dummy_reader'] = user_input['dummy_reader']

#instruction for layer 2
Instruction_dict.values['max_draw_down'] = user_input['capital'] * 0.1
#risk aversion is divided by 2, to avoid a high initial trading thesholds and therefore trading block by this parameter
Instruction_dict.values['risk_aversion'] = 0.25
Instruction_dict.values['stoploss'] = 10

#instruction for layer 1
Instruction_dict.values['learn'] = 0.65
Instruction_dict.values['adaption'] = 0.5
Instruction_dict.values['transactionCost'] = 0.001
Instruction_dict.values['weightDecay'] = 1
Instruction_dict.values['m'] = user_input['m']
Instruction_dict.values['account_val'] = Instruction_dict.values['capital']
#init FX_Reader and sender
#init the rest of parameters
#send the dictionary
sender_receiver = sr.Sender_Receiver()
sender_receiver.readysend()
#optimizer = os.Optimization_System(instruction_dict['anti_risk'],instruction_dict['capital'])
reader = fxr.FX_Reader()

# while(True):
# 
#     if('ERROR' in instruction_dict):
#             UI.printErr()
#     else:
#         if(tstep%9000 == 0):
#             UI.print_info_intro()
#         if(tstep%180 == 0):
#             UI.print_info(instruction_dict)
# 
#         #change params and send
#         if(tstep >= 10000):
#             instruction_dict = optimizer.optimize(instruction_dict)
# 
#         #change params and send
#         instruction_dict = optimizer.optimize(instruction_dict)
#         instruction_dict['long_price'],instruction_dict['short_price'] = reader.readPrice()
#         sender_receiver.send(instruction_dict)
#     tstep += 1
#     instruction_struct = ""
#     while(instruction_struct == ""):
#         instruction_struct = sender_receiver.receive()
#         if instruction_struct == "":
#             time.sleep(1)

while(True):
    Instruction_dict.values['long_price'],Instruction_dict.values['short_price'] = reader.readPrice()
    sender_receiver.send(Instruction_dict.values)
    time.sleep(1)
