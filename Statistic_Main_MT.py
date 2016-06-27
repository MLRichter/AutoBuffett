__author__ = 'matsrichter'
import LayerWrappers.Layer1_Test_Object as l1
import LayerWrappers.Layer2_Test_Object as l2
import LayerWrappers.Layer3_Test_Object as l3
import LayerWrappers.Communicator_Test as com
import threading
import Statrec_Toolbox_Object as tb
import numpy as np
import sys
#import twitter
#import random as r
#import Layer3
#import time as time
from tweepy import *

def init_instructionDict(i = 1,j = 1):
    instruction_dict = dict()
    global f_name
    global profit_list


    #initialize the instruction_dict and layer 1 params
    instruction_dict['capital'] = 1000
    instruction_dict['account_val'] = 1000
    instruction_dict['anti_risk'] = 0.5
    instruction_dict['symbol'] = f_name

    #DEBUG
    instruction_dict['DEBUG'] = True
    instruction_dict['lever'] = 1
    instruction_dict['dummy_reader'] = 'y'
    instruction_dict['AdaBoost'] = 0
    #RLL(1) Random(2) SVM(3) RSVM(4) RLLSVM(5) B&H(6) NLSVM(7) Poly(8) MLP(9)
    instruction_dict['learner'] = 7
    
    #Learner9 (MLP) specific stuff
    instruction_dict['w_size'] = 1000
    instruction_dict['layers'] = 4
    #instruction for layer 2
    instruction_dict['max_draw_down'] = instruction_dict['capital'] * (0.07)
    #risk aversion is divided by 2, to avoid a high initial trading thesholds and therefore trading block by this parameter
    instruction_dict['risk_aversion'] = 0.5
    instruction_dict['stoploss'] = 50
    
    instruction_dict['poly'] = 10
    instruction_dict['epoch'] = 40000

    #instruction for layer 1
    instruction_dict['learn'] = 0.001
    #instruction_dict['learn'] = 0.01
    instruction_dict['adaption'] =0.5#0.9
    instruction_dict['transactionCost'] = 0.001
    instruction_dict['weightDecay'] = 1
    #Number of Neuron (per Layer in a MLP)
    instruction_dict['m'] = 30
    instruction_dict['account_val'] = instruction_dict['capital']
    instruction_dict['long_price'] = 0
    instruction_dict['short_price'] = 0
    return instruction_dict

def run(threadId = 0):    
    global profit_list
    global best
    global worst
    date_labels = list()
    price = list()
    
    for i in range(100):
        #UPDATE thread status
        lock.acquire()
        global it
        it += 1 
        lock.release()
            
        #initialize instruction dict
        print("[Thread "+str(threadId)+'] start processing experiment no. '+str(it))
        instructionDict = init_instructionDict(threadId+1,i)
        instructionDict['iteration'] = i
        #start tracking stats
        stat = tb.Toolbox(instructionDict)
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
                profit_list.append(instructionDict['account_val'])
                break
        #store test results
        #stat.print_and_save(instructionDict)
        print("[Thread "+str(threadId)+'] finished experiment, with result: '+str(instructionDict['account_val']))
        lock.acquire()                  
#        if(it%10 == 0):
#            api.send_direct_message('Vangrand1',text="[Thread "+str(threadId)+'] Experiment progress: '+str(it)+"%")            
        save_result(instructionDict['account_val'])
        if(instructionDict['account_val'] > best):
            best = instructionDict['account_val']
            stat.save_csv('best',instructionDict)
        elif(instructionDict['account_val'] < worst):
            worst = instructionDict['account_val']
            stat.save_csv('worst',instructionDict)
        lock.release()
            
def process_result():
    global profit_list
    
    global mu
    mu = np.mean(profit_list)   
    
    global median
    median = np.median(np.array(profit_list))
    
    global sigma
    sigma = np.std(profit_list)
    return

def save_result(result):
    f = open('stat_dump/'+f_name+"_final.txt",'a')
    global it   
    f.write(str(it)+' '+str(result)+'\n')
    f.close()
    return
    
    
#current iteration
global it
#middle value of final profit
global mu
#standard devitation
global sigma
#median of final profit
global median
#best experiment result
global best
#worst experiment result
global worst
#list of result
global profit_list
#name of file
global f_name

# Twitter embedded
global api
#ACCESS_TOKEN =  'XYZ'
#ACCESS_SECRET= 'XYZ'
#CONSUMER_KEY = 'XYZ'
#CONSUMER_SECRET = 'XYZ'
#auth  = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
#api = API(auth)


#Initi file
f_name = 'NLSVMw1000'
profit_list = list()
best = 0
worst = 2000
it = 0
k = 1
lock = threading.Lock()
threads = list()
for i in range(k):
    t = threading.Thread(target=run,args=(i,))
    t.start()
    threads.append(t)
                
for i in threads:
    try:
        i.join()
    except SystemExit:
#        api.send_direct_message('Vangrand1',text="[Thread MAIN] CRITITCAL ERROR")
        print("Attempted System Exit")
        
process_result()
f = open('stat_dump/'+f_name+"_final.txt",'a')
f.seek(0,2)
for i in range(50):
    f.write('#')
f.write('\n')
f.write("mu_profit: "+str(mu)+"\n")
f.write("sigma:     "+str(sigma)+'\n')
f.write('median:    '+str(median)+"\n")
f.write('best:      '+str(best)+"\n")
f.write('worst:     '+str(worst)+"\n")
f.close()
#api.send_direct_message('Vangrand1',text="[Thread MAIN] Experiment finished: \nbest: "+str(best)+'\naverage: '+str(mu)+'\nworst: '+str(worst))