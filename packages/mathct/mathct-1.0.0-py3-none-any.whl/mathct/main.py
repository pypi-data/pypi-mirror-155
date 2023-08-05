# -*- coding: utf-8 -*-
"""@author :- Dharmendra Choudhary
"""

import pandas as pd

df = pd.read_csv(r'C:\Users\dnc11\git_projects\mathct\dependencies\mathematical_constants.csv',encoding= 'unicode_escape')

constants_dict = { k:v for (k,v) in zip(df["constant "],df["constant_value"])} 

def constant_help():
    print("To get the value of a particular constant, please use constant from the list below and use constant function \n")
    print("The List of constant with values is as follows: \n")
    print("Constant \t Value \n")
    for i in constants_dict:        
        print(i,": ",constants_dict[i])


def constants(c):
    return constants_dict[c]




