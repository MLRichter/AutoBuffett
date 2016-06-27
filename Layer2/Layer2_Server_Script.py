__author__ = 'matsrichter'

import Account as acc
import Sender_Receiver as sr
import Risk_Manager as rm
import time as time

# Connect here with Layer 3 and Layer 1 - Not implemented yet
sender_receiver = sr.Sender_Receiver()
instruction_struct = ""
while(instruction_struct == ""):
    instruction_struct = sender_receiver.receive()
    if instruction_struct == "":
        time.sleep(1)
#time = time.time()
symbol = instruction_struct['symbol']
capital = instruction_struct['capital']
account = acc.Account(symbol,capital,time.time(),instruction_struct['short_price'],
                      instruction_struct['long_price'],instruction_struct['stoploss'])
risk_manager = rm.Risk_Manager(account,instruction_struct['risk_aversion'],instruction_struct['max_draw_down'])
tstep = time.time()

# the core-execution loop
while(True):
    instruction_struct = sender_receiver.receive()
    if instruction_struct == "":
        time.sleep(1)
        continue
#    time = time.time()

    #update account
    account.symbol = instruction_struct['symbol']
    account.update(instruction_struct['short_price'],instruction_struct['long_price'],tstep)
    account.stoploss = instruction_struct['stoploss']

    #update risk manager
    risk_manager.risk_aversion = instruction_struct['risk_aversion']
    risk_manager.max_draw_down = instruction_struct['max_draw_down']

    l1_decision = instruction_struct['decision']

    #check fatal error-state of finances
    risk_manager.check_broke(l1_decision)
    print l1_decision
    #if Broke, close exsisting position for exiting
    if(risk_manager.isBroke):
        instruction_struct['ERROR'] = "isBroke"
        account.sell_all()
    #evaluate risk and execute decision if needed
    if(risk_manager.eval_risk(l1_decision)):
        if(l1_decision > 0):
            account.execute('long')
        else:
            account.execute('short')

    #send decision
    instruction_struct['account_val'] = account.total_account_value()
    instruction_struct['capital'] = account.capital
    sender_receiver.send(instruction_struct)