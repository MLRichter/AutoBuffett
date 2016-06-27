__author__ = 'matsrichter'
import numpy as np
import  UI

test_dict = dict()
capital = range(0,1000,1)
total_account_val = range(0,2000,2)
test_dict['capital'] = 1000
UI.print_info_intro(True)
for i in range(len(capital)):
    test_dict['capital'] = capital[i]
    test_dict['account_val'] = total_account_val[i]
    if((i+1)%25 == 0):
        UI.print_info_intro(True)
    UI.print_info(test_dict)
