import pandas as pd
import numpy as np
from pandas import ExcelWriter
##Lithology Logging Sheet
lith = pd.read_excel("Lithology_Field Logging Sheet.xlsx", header=None, skiprows=8, usecols = "A:P", names = ['Depth', 'Lithology','Scode','Smod','Shade','Colour','Min','Max','Roundness','Sorting','Texture','Structure','Contact','Fraction','Alteration','Strength'])

##Structural Features Logging Sheet (v.5-no merged column, use column headers)
struct = pd.read_excel("Structural Features_Field Logging Sheet.xlsx", header=None, skiprows=8, usecols = "A:Q", names = ['Defect','Type','RHS','Top','LHS','Separation','Roughness','Planarity','Period','Undulation','Angle','Alteration','Material','Area','Shade','Colour','Moisture'])

#Difference between Distance to Top of defect
def cal_spacing():
    for i in range (0,len(struct)):
        spacing = (struct['Top'] - struct['Top'].shift(1))*1000
    

for i in range(0,len(struct)):
    if cal_spacing() <= 60:
        A3 = 5
        print (A3)
    elif 60 < cal_spacing() <= 200:
        A3 = 8
        print (A3)
    elif 200 < cal_spacing() <= 600:
        A3 = 10
        print (A3)
    elif 600 < cal_spacing() <= 2000:
        A3 = 15
        print (A3)
    elif 2000 < cal_spacing():
        A3 = 20
        print (A3)	
