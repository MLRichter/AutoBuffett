__author__ = 'matsrichter'

import Layer3.UI as UI
import Layer3.Optimization_System as opt_sys
#import Layer3.fxr_dummy as fxr_d
#import Layer3.sine_reader as fxr_d
import Layer3.benchmark_reader as fxr_d
import Layer3.FX_Reader as fxr
import Communicator_Test as com
import random as r
import matplotlib.pylab as plt


class Layer3:

    def __init__(self,instruction_dict,communicator=None):

        self.tstep = 0
        self.optimizer = opt_sys.Optimization_System(instruction_dict['anti_risk'],instruction_dict['capital'])
        if(instruction_dict['DEBUG'] and instruction_dict['dummy_reader'] == 'y'):
            self.fx_reader = fxr_d.FX_Reader()
        else:
            self.fx_reader = fxr.FX_Reader()
        self.communicator = communicator
        self.decision_list = list() #historical decsision
        self.price_list = list()    #historical prices
        self.date_list = list()     #timestamps
        self.acc_list = list()      #total account value

    def adCom(self, communicator):
        assert(isinstance(communicator,com.Sender_Receiver))
        self.communicator = communicator
        
    def print_decision(self):
        #fig1 = plt.figure()
        #ax1 = fig1.add_subplot(111)
        #ax1.plot(range(len(self.decision_list)),self.decision_list)
        #fig2 = plt.figure()
        #ax2 = fig2.add_subplot(111)
        #ax2.plot(range(len(self.price_list)),self.price_list)
        fig3 = plt.figure()
        ax3 = fig3.add_subplot(111)
        ax3.plot(range(len(self.acc_list)),self.acc_list)

    def call(self,instruction_dict):
        #check for errors
        if('ERROR' in instruction_dict):
            #self.print_decision()
            UI.printErr(instruction_dict['ERROR'])
            return
        else:
#            if(self.tstep%3000 == 0 and self.tstep > 20000):
#                UI.print_info_intro()
#            if(self.tstep%300 == 0) and self.tstep > 20000:
#                UI.print_info(instruction_dict)

            #change params and send
            if(self.tstep >= 20000):
                instruction_dict = self.optimizer.optimize(instruction_dict)
            try:
                #read tuple from reader:
                tmp = self.fx_reader.readPrice()
                instruction_dict['long_price'] = tmp[0]
                instruction_dict['short_price'] = tmp[1]
                instruction_dict['tstep'] = tmp[2]
                #self.date_list.append(tmp[2])
            except:
             #   self.print_decision()
                
                instruction_dict['ERROR'] = "EoF"
                return
                
            #adjust prices by lever
            instruction_dict['long_price'] = instruction_dict['long_price']
            instruction_dict['short_price'] = instruction_dict['short_price']

            self.communicator.send(instruction_dict,'l1')
            #self.decision_list.append(instruction_dict['decision'])
            #self.price_list.append(instruction_dict['long_price'])
            #self.acc_list.append(instruction_dict['account_val'])
            self.tstep += 1
            #early bird error check
            if('ERROR' in instruction_dict):
                #self.print_decision()
                UI.printErr(instruction_dict['ERROR'])
                return