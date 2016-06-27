__author__ = 'matsrichter'

import Optimization_System as os
import UI
import FX_Reader as fxr
import Sender_Receiver as sr
import time as time

user_input = UI.introduction()
tstep = 0

instruction_dict = dict()
#initialize the instruction_dict and layer 1 params
user_input = UI.introduction()
instruction_dict['capital'] = user_input['capital']
instruction_dict['account_val'] = user_input['capital']
instruction_dict['anti_risk'] = user_input['anti_risk']
instruction_dict['symbol'] = user_input['symbol']

#DEBUG
instruction_dict['DEBUG'] = user_input['DEBUG']
instruction_dict['lever'] = user_input['lever']
instruction_dict['dummy_reader'] = user_input['dummy_reader']

#instruction for layer 2
instruction_dict['max_draw_down'] = user_input['capital'] * 0.1
#risk aversion is divided by 2, to avoid a high initial trading thesholds and therefore trading block by this parameter
instruction_dict['risk_aversion'] = 0.5
instruction_dict['stoploss'] = 10

#instruction for layer 1
instruction_dict['learn'] = 0.65
instruction_dict['adaption'] = 0.5
instruction_dict['transactionCost'] = 0.001
instruction_dict['weightDecay'] = 1
instruction_dict['m'] = user_input['m']
instruction_dict['account_val'] = instruction_dict['capital']
#init FX_Reader and sender
#init the rest of parameters
#send the dictionary
sender_receiver = sr.Sender_Receiver()
optimizer = os.Optimization_System(instruction_dict['anti_risk'],instruction_dict['capital'])
reader = fxr.FX_Reader()

while(True):

    if('ERROR' in instruction_dict):
            UI.printErr()
    else:
        if(tstep%9000 == 0):
            UI.print_info_intro()
        if(tstep%180 == 0):
            UI.print_info(instruction_dict)

        #change params and send
        if(tstep >= 10000):
            instruction_dict = optimizer.optimize(instruction_dict)

        #change params and send
        instruction_dict = optimizer.optimize(instruction_dict)
        instruction_dict['long_price'],instruction_dict['short_price'] = reader.readPrice()
        sender_receiver.send(instruction_dict)
    tstep += 1
    instruction_struct = ""
    while(instruction_struct == ""):
        instruction_struct = sender_receiver.receive()
        if instruction_struct == "":
            time.sleep(1)

