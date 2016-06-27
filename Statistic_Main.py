__author__ = 'matsrichter'
import LayerWrappers.Layer1_Test_Object as l1
import LayerWrappers.Layer2_Test_Object as l2
import LayerWrappers.Layer3_Test_Object as l3
import LayerWrappers.Communicator_Test as com
import Statrec_Toolbox as stat
import numpy as np
#import random as r
#import Layer3
#import time as time

def init_instructionDict(i = 1,j = 1):
    instruction_dict = dict()



    #initialize the instruction_dict and layer 1 params
    instruction_dict['capital'] = 1000
    instruction_dict['account_val'] = 1000
    instruction_dict['anti_risk'] = 0.5
    instruction_dict['symbol'] = 'sine_bull(1)'

    #DEBUG
    instruction_dict['DEBUG'] = True
    instruction_dict['lever'] = 1
    instruction_dict['dummy_reader'] = 'y'
    instruction_dict['AdaBoost'] = 0
    #RLL(1) Random(2) SVM(3) RSVM(4) RLLSVM(5) B&H(6) NLSVM(7) Poly(8) MLP(9)
    instruction_dict['learner'] = 1
    
    #Learner9 (MLP) specific stuff
    instruction_dict['w_size'] = 100
    instruction_dict['layers'] = 4
    #instruction for layer 2
    instruction_dict['max_draw_down'] = instruction_dict['capital'] * (0.1)
    #risk aversion is divided by 2, to avoid a high initial trading thesholds and therefore trading block by this parameter
    instruction_dict['risk_aversion'] = 0.5
    instruction_dict['stoploss'] = 100
    
    instruction_dict['poly'] = 6
    instruction_dict['epoch'] = 20000

    #instruction for layer 1
    instruction_dict['learn'] = 0.001
    #instruction_dict['learn'] = 0.01
    instruction_dict['adaption'] = 0.1#0.9
    instruction_dict['transactionCost'] = 0.001
    instruction_dict['weightDecay'] = 1
    #Number of Neuron (per Layer in a MLP)
    instruction_dict['m'] = 30
    instruction_dict['account_val'] = instruction_dict['capital']
    instruction_dict['long_price'] = 0
    instruction_dict['short_price'] = 0
    return instruction_dict
    
end_prices = list()
date_labels = list()
price = list()

for j in range(1):
    for i in range(1):
        #initialize instruction dict
        instructionDict = init_instructionDict(i,j)
        instructionDict['iteration'] = i
        #start tracking stats
        stat.init(instructionDict)
        #init layer-objects
        layer3 = l3.Layer3(instructionDict)
        layer2 = l2.Layer2(instructionDict)
        layer1 = l1.Layer1(instructionDict)
        #wire them together via communicator
        communicator = com.Sender_Receiver(layer1,layer2,layer3)
        layer1.adCom(communicator)
        layer2.adCom(communicator)
        layer3.adCom(communicator)
        
        while(True):
            #execute  single price cycle
            layer3.call(instructionDict)
            #record stats
            stat.update(instructionDict)
            #print("ROUND")
            if('ERROR' in instructionDict):
                end_prices.append(instructionDict['account_val'])
                stat.eof_shutdown()
                break
        #store test results
        #stat.print_and_save(instructionDict)
    
    s = "\n\n TOTAL STATS FOR ITERATION: "+str(j)+"\n\n Average End: "+str(np.mean(end_prices))+"\n"+"Best: "+str(np.amax(end_prices))+"\n Worst: "+str(np.amin(end_prices))
    stat.print_and_save(instructionDict)    
    stat.print_special(s)
stat.final_shutdown()
    
