# Strength of intact rock material (A1)
import pandas as pd
import numpy as np
from pandas import ExcelWriter

##Lithology Logging Sheet
#lithhead = pd.read_excel("Lithology_Field Logging Sheet.xlsx", header=None, skiprows=0, nrows = 5, na_value=["not available","n.a.",""], comment="Comment")
lith = pd.read_excel("Lithology_Field Logging Sheet.xlsx", header=None, skiprows=8, usecols = "A:P", names = ['Depth', 'Lithology','Scode','Smod','Shade','Colour','Min','Max','Roundness','Sorting','Texture','Structure','Contact','Fraction','Alteration','Strength'])
struct = pd.read_excel("Structural Features_Field Logging Sheet.xlsx", header=None, skiprows=8, usecols = "A:Q", names = ['Defect','Type','RHS','Top','LHS','Separation','Roughness','Planarity','Period','Undulation','Angle','Alteration','Material','Area','Shade','Colour','Moisture'])

print ('Press "A" if you would like to enter an UCS value or')
print ('Press "B" if you would like to use the Estimated Strength value from Lithology Logging Sheet')
res = str(input('YOUR RESPONSE: '))

## If the user input a UCS value for all the structural features
if res in ['A', 'a']:
    UCS = float(input('Enter Uniaxial Compressive Strength, UCS (MPa): '))
    if UCS < 1:
        A1 = 0
    elif 1 <= UCS < 5:
        A1 = 1
    elif 5 <= UCS < 25:
        A1 = 2
    elif 25 <= UCS < 50:
        A1 = 4
    elif 50 <= UCS < 100:
        A1 = 7
    elif 100 <= UCS < 250:
        A1 = 12
    else:
        A1 = 15
		
    for i in range(0,len(struct)):
        print (A1)	
		
## If the user wants to use the UCS from Estimated Strength in Lithology Logging Sheet
elif res in ['B', 'b']:
    def get_str(dis,lith):
        for i in range(0,len(lith)):
            if i == 0:
                if 0 < dis <= lith.Depth[i]:
                    return lith.Strength[i]
            elif lith.Depth[i-1] < dis <= lith.Depth[i]:
                return lith.Strength[i]

    for i in range(0,len(struct)):
        if get_str(struct.Top[i],lith) == 'VL':
            A1 = 0
            print (A1)
        elif get_str(struct.Top[i],lith) == 'LO':
            A1 = 1
            print (A1)
        elif get_str(struct.Top[i],lith) == 'ME':
            A1 = 2
            print (A1)
        elif get_str(struct.Top[i],lith) == 'HI':
            A1 = 4
            print (A1)
        elif get_str(struct.Top[i],lith) == 'VH':
            A1 = 7
            print (A1)
        elif get_str(struct.Top[i],lith) == 'EH':
            A1 = 15
            print (A1)

# Write result back to Excel
writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
struct.to_excel(writer, index=False, sheet_name = 'Sheet1', columns=['Defect Number','Type'])
writer.save()			


