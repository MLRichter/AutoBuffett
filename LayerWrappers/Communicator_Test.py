__author__ = 'matsrichter'

class Sender_Receiver:

    def __init__(self,l1,l2,l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    def send(self,instruction_struct,destination_layer_id):
        if(destination_layer_id == 'l1'):
            self.l1.call(instruction_struct)
        elif(destination_layer_id == 'l2'):
            self.l2.call(instruction_struct)
        elif(destination_layer_id == 'l3'):
            return instruction_struct