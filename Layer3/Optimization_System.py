__author__ = 'matsrichter'

import numpy as np


class Optimization_System:
    def __init__(self, anti_risk, start_capital):
        self.current_cycle = 0
        self.current_subcylce = 0
        self.current_subsubcycle = 0

        self.parameters = ['learn', 'adaption', 'transactionCost', 'weightDecay', 'stoploss','risk_aversion']
        self.cycle_size = 6  # number of parameters to optimize
        self.mutation_number = 15  # Number of mutations per parameter
        self.subsubcycle_size = 1000  # Iterations per mutation
        self.anti_risk = anti_risk
        self.capital = start_capital

        # this value chronic keeps track of that account_values of one cycle
        # more would be a waste of memory, since this chronic is only for evaluating the utility function
        self.account_value_chronic = list()
        self.account_value_chronic.append(self.capital)
        self.current_cycle_mutations = self.get_mutations(0.65)

    # this function optimizes a single parameter. Every parameter has 15 mutations and every mutation is used 50 cycles
    # this functions keeps track of the switching and using the most optimal parameters after gathering performance data
    # function behavior goes threw three cycles:
    #   Cycle:          Size: number of parameters (indicated by current cycle
    #   Subcycle:       15 Iterations over all mutations of the cycle-parameter
    #   Subsubcycle:    50 Iterations are executed on every parameter, gathering information
    def optimize(self, instruction_dict):
        assert (isinstance(instruction_dict, dict))
        #this keeps track of the current cycle, subcycle and subsubcycle
        if (self.current_subsubcycle >= 1000):
            self.current_subcylce += 1
            self.current_subsubcycle = 0
            if (self.current_subcylce >= self.mutation_number):
                #use best scoring value
               # self.account_value_chronic.append(instruction_dict['total_account_value'])
                instruction_dict[self.parameters[self.current_cycle]] = self.eval_best()
                self.current_cycle += 1
                self.current_subcylce = 0
                if (self.current_cycle >= self.cycle_size):
                    self.current_cycle = 0
                #generate new mutations
                self.current_cycle_mutations = self.get_mutations((instruction_dict[self.parameters[self.current_cycle]]))
            #add new mutation of current parameter
            instruction_dict[self.parameters[self.current_cycle]] = self.current_cycle_mutations[self.current_subcylce]
        self.account_value_chronic.append(instruction_dict['account_val'])
        if(len(self.account_value_chronic) > self.cycle_size*self.subsubcycle_size*self.mutation_number*2):
            self.account_value_chronic.pop(0)
        self.current_subsubcycle += 1
        return instruction_dict

    # calculates the returns needed for the utility function in several occasion
    # @input mutation_number    indexes the time frame with size 100 by the active mutation at this point of time
    def get_return_chronic(self, mutation_number):
        total_returns = list()
        for i in range(1000*mutation_number,(mutation_number+1)*1000):
            wealth = self.account_value_chronic[i + 1] - self.account_value_chronic[i]
            total_returns.append(wealth)
        return total_returns

    # calculations the average return as part of the risk-ratio
    #   @input mutation_number  determines the time period
    def get_average_return(self, mutations_number):
        total_returns = self.get_return_chronic(mutations_number)
        total = 0
        for i in total_returns:
            total += i
        return total / len(total_returns)

    # calculates the risk ratio as part of the utility function
    # @input mutation_number    determines the time period by the active mutation
    def risk_ratio(self, mutation_number):
        positive = 0
        negative = 0
        returns = self.get_return_chronic(mutation_number)
        for i in returns:
            if (i >= 0):
                positive += (i * i)
            elif (i < 0):
                negative += (i * i)
        if (positive == 0):
            return negative
        return negative / positive

    #utility-function for evaluation the best mutation of the parameter
    #   @input mutation number: determines one of the 15 mutations
    def utility(self, mutation_number):
        a = 1
        avg_return = a*(1-self.anti_risk) * self.get_average_return(mutation_number)
        risk_ratio = self.anti_risk * self.risk_ratio(mutation_number)
        return (a * (1 - self.anti_risk) * self.get_average_return(mutation_number)) - (
            self.anti_risk * self.risk_ratio(mutation_number))

    #evaluates best performing mutation and resets the account_value_chronic
    def eval_best(self):
        best_score = 0
        best_val = 0
        index = 0
        for i in range(len(self.current_cycle_mutations)):
            score = self.utility(i)
            if (score > best_score) or i == 0:
                best_val = self.current_cycle_mutations[i]
                best_score = self.utility(i)
                index = i
        last_val = self.account_value_chronic[len(self.account_value_chronic)-1]
        self.account_value_chronic = list()
        self.account_value_chronic.append(last_val)
#        print("Best is :"+str(best_val)+" with the score: "+str(best_score)+ " with index: "+ str(index)  +
#              "for parameter: "+ self.parameters[self.current_cycle])
        return best_val

    #mutates the given parameter and returns the mutated values
    def mutate(self, value):
        #maybe sigma = 1 used to be 0.2???
        if(self.current_cycle == 0):
            mutation = value + np.random.normal(0,0.001)
            if(mutation >= 1):
                return 1
            elif(mutation <= 0):
                return 0.0001
            else:
                return mutation
        elif(self.current_cycle == 1):
            mutation = value + np.random.normal(0,0.05)
            if(mutation >= 0.5):
                return 0.5
            elif(mutation <= 0.0001):
                return 0.0001
            else:
                return mutation
        elif(self.current_cycle == 2):
            mutation = value + np.random.normal(0,1)
            if(mutation >= 10):
                return 10
            elif(mutation <= 0):
                return 0.0001
            else:
                return mutation
        elif(self.current_cycle == 3):
            return 1                           #weightDecay currently disabled
        elif(self.current_cycle == 4):
            mutation = value + np.random.normal(0,5)
            if(mutation >= 200):
                return 200
            elif(mutation <= 0):
                return 20
            else:
                return mutation
        elif(self.current_cycle == 5):
            mutation = value + np.random.normal(0,0.05)
            if(mutation >= 1):
                return 1
            elif(mutation <= 0):
                return 0.0001
            else:
                return mutation

    def get_mutations(self,value, number = 15):
        mutation_list = list()
        mutation_list.append(value)
        for i in range(number-1):
            mutation_list.append(self.mutate(value))
        return mutation_list
