from __future__ import print_function

import matplotlib.pylab as plt
import multiprocessing as mp
__author__ = 'matsrichter'

names = ['Capital','Total Value','Invested','Current Profit', 'Price']
total_len = len(names[0])+len(names[1])+len(names[2])+len(names[3])+len(names[4]) + 30
last_capital_val = 0
capital_list = list()

def introduction():
    print("FX-Trading System started")
    print("Please set parameters:")
    print("----------------------")
    forex_symbol = str(raw_input("Enter valid fx-symbol (example: EURUSD): "))

    print("")
    
    learner = int(raw_input("RLL(1) Random (2) SVM(3) RSVM(4) RLLSVM(5) B&H(6) NLSVM(7): "))

    debug = None
    while(debug == None):
        debug_instruction = str(raw_input("Enable Debug Mode?: y/n: "))
        if(debug_instruction == "y"):
            debug = True
        elif(debug_instruction == "n"):
            debug = False

    risk_val = float(raw_input("Enter risk aversion parameter between 1 and 0. 0 = extremly risky, 1 = extremly carefull: "))
    while(risk_val < 0 or risk_val > 1):
        risk_val = float(raw_input("Invalid, try again: "))
    capital = -1
    while(capital < 0):
        capital = float(raw_input("Please Enter your start capital in units of the fx-index home currency: "))
    m = 0
    while(m <= 0):
        m = int(raw_input("Please enter the number of neurons (8-12): "))

    lever = 0
    AdaBooster = -1
    if(debug):
        while(lever <= 0):
            lever  = int(raw_input("Please enter lever (profit/loss multiplier, default is 1): "))
        #f(str(raw_input("use AdaBoost? (y/n): ")) == 'y'):
         #   AdaBooster = int(raw_input("Please enter number of learners: "))
    while(AdaBooster < 0):
        AdaBooster = int(raw_input("Please enter number of NN for AdaBoosting (0 = disable AdaBoosting): "))

    if(lever == 0):
        lever = 1

    dr = None
    while dr != 'y' and dr != 'n':
        dr = str(raw_input("Dummy Reader (y/n)?: "))

    proto_instruction = dict()
    proto_instruction['DEBUG'] = debug
    proto_instruction['AdaBoost'] = AdaBooster
    proto_instruction['dummy_reader'] = dr
    proto_instruction["capital"] = capital
    proto_instruction['anti_risk'] = risk_val
    proto_instruction['symbol'] = forex_symbol
    proto_instruction['m'] = m
    proto_instruction['lever'] = lever
    proto_instruction['learner'] = learner

    last_capital_val = capital
    return proto_instruction


def print_info_intro(seperator = True):
    global names
    global total_len
    if(seperator):
        for i in range(total_len):
            print("-",end="")
        print()
    for i in names:
        print(i,end="          ")
    for i in range(total_len):
        print(" ",end="")
    print()
    if(seperator):
        for i in range(total_len):
            print("-",end="")
        print()
#    print_tables()


def print_tables():
    global capital_list
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(range(len(capital_list)),capital_list)
    plt.xlabel('time in price-updates')
    plt.ylabel('total account value')
    plt.axis('tight')
    plt.draw()
    return

def print_info(instruction_set):
    capital = (instruction_set['capital'])
    print_table_part(0,capital)
    print_table_part(1,instruction_set['account_val'])
    print_table_part(2,instruction_set['account_val']-instruction_set['capital'])
    global last_capital_val
    global capital_list
    capital_list.append(instruction_set['account_val'])
    if(len(capital_list) > 1800):
        capital_list.pop(0)
    current_profit = instruction_set['account_val'] - last_capital_val
    print_table_part(3,current_profit,True)
    print_table_part(4,instruction_set['long_price'])
    print()
    last_capital_val = instruction_set['account_val']
    return

def print_table_part(name_index, value,plus_minus = False):
    global names
    if plus_minus and value > 0:
        val_str = "+"+str(value)
    else:
        val_str = str(value)
    print(val_str, end="")
    if(len(names[name_index])+10-len(val_str)) > 0:
        for i in range(len(names[name_index])+10-len(val_str)):
            print(" ",end="")

def printErr(msg):
    print("Error: "+msg)