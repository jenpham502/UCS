#def generate_input1():
# Generate Input 1
import pandas as pd
import xlsxwriter

inp1 = pd.DataFrame()

#-----------Bolted Interval----------
print ('What is the depth to the roof line (in metres)?')
roofdepth = float(input('YOUR RESPONSE: '))

print ('What is the roof bolt length (in metres)?')
boltlength = float(input('YOUR RESPONSE: '))

topbolt = roofdepth - boltlength
#-----------Define structural units----------
#A structural unit generally contains one lithologic layer, but several rock layers may be lumped together
#if their engineering properties are similar.
print('The CMRR is determined by averaging all the Unit Ratings within the bolted interval.')
print('A structural unit generally contains one lithologic layer, but several rock layers may be lumped together if their engineering properties are similar.')

print('How many structural units are there from', topbolt, 'to', roofdepth, 'metre?')
NOU = int(input('YOUR RESPONSE: '))

enddepth = []
startdepth = []
thickness = []

if NOU == 1:
    startdepth = float(roofdepth)
    enddepth = float(startdepth) - float(boltlength)
    inp1.at[1, 'Unit'] = '1'
    inp1.at[1, 'Start Depth'] = startdepth
    inp1.at[1, 'End Depth'] = enddepth
    inp1.at[1, 'Thickness'] = boltlength

else:
    for i in range(0, NOU-1, 1):
        print('Structural Unit is counted upward from immediate roof, starting from 1.')
        print('What is the thickness of structural unit', i+1,'(in metres)?')
        temp = float(input('YOUR RESPONSE: '))
        enddepth.append(temp)
        startdepth.append(temp)
        thickness.append(temp)

    inp1['Unit'] = '0'
    inp1['Start Depth'] = '0'
    inp1['End Depth'] = '0'
    inp1['Thickness'] = '0'
    for i in range(0, NOU, 1):
        if i == 0:
            unit = i+1
            startdepth[0] = roofdepth
            enddepth[i] = startdepth[i] - thickness[i]
            print('Start depth of structural unit', unit, 'is', startdepth[i])
            print('End depth of structural unit', unit, 'is', enddepth[i])
        elif 0 < i < NOU-1:
            unit = i + 1
            startdepth[i] = enddepth[i-1]
            enddepth[i] = startdepth[i] - thickness[i]
            print('Start depth of structural unit', unit, 'is', startdepth[i])
            print('End depth of structural unit', unit, 'is', enddepth[i])
        else:
            enddepth.append(0)
            startdepth.append(0)
            thickness.append(0)
            unit = i + 1
            startdepth[i] = enddepth[i-1]
            enddepth[i] = float(topbolt)
            thickness[i] = startdepth[i] - enddepth[i]
            print('Start depth of structural unit', unit, 'is', startdepth[i])
            print('End depth of structural unit', unit, 'is', enddepth[i])

        inp1.at[i, 'Unit'] = unit
        inp1.at[i,'Start Depth'] = startdepth[i]
        inp1.at[i,'End Depth'] = enddepth[i]
        inp1.at[i, 'Thickness'] = thickness[i]

inp1['UCS'] = '0'
inp1['DPLT'] = '0'
inp1['RQD'] = '0'
inp1['FS'] = '0'
inp1['Moisture'] = '0'
for i in range(1, NOU+1):
#----------UCS----------
    print('What is the Uniaxial Compressive Strength, UCS (in MPa) for structural unit ', i, '?')
    print("Enter 'VL' for 0.6-2 MPa, 'LO' for 2-6 MPa, 'ME' for 6-20 MPa, 'HI' for 20-60 MPa, 'VH' for 60-200 MPa, 'EH' for >200 MPa")
    UCS = str(input('YOUR RESPONSE: '))

    inp1.at[i, 'UCS'] = UCS

#----------DPLT----------
    print('What is the Diamentral Point Load Test Strength (in MPa) for structural unit ', i, '?')
    DPLT = float(input('YOUR RESPONSE: '))
    inp1.at[i, 'DPLT'] = DPLT
#----------RQD & FS----------
    print("Were there any fractures observed in structural unit ", i, "? Enter 'Y' for yes or 'N' for no.")
    res = str(input('YOUR RESPONSE: '))
    if res in ['Y', 'y']:
        print('What is the Rock Quality Designation, RQD (%) for structural unit ', i, '?')
        RQD = int(input('YOUR RESPONSE: '))
        inp1.at[i, 'RQD'] = RQD
        if RQD <= 90:
            FS = 0
            inp1.at[i, 'FS'] = FS
        else:
            print('Fracture spacing is easily determined by counting the core breaks in a particular unit and then dividing by the thickness of the unit.')
            print('What is the Fracture Spacing, FS (in mm) for structural unit ', i, '?')
            FS = input('YOUR RESPONSE: ')
            inp1.at[i, 'FS'] = FS
    elif res in ['N','n']:
        RQD = 'N/A'
        inp1.at[i, 'RQD'] = RQD
        FS = 'N/A'
        inp1.at[i, 'FS'] = FS
    else:
        print ('Error! Check your response and try again.')

#----------Moisture----------
# Moisture Sensitivity Deduction (MSD)(only applies when unit forms the immediate roof or
# if water is leaking through the bolted interval.)
print("Is the water leaking through the bolted interval? Enter 'Y' for yes or 'N' for no.")
res = str(input('YOUR RESPONSE: '))

if res in ['Y', 'y']:
# MSD will be applied to all the units
    for i in range(1, NOU+1):
        print('What is the Moisture Sensitivity of structural unit', i,'?')
        print("Enter 'NS' for Not sensitive, 'SS' for Slightly sensitive,")
        print("'MS' for Moderate sensitive, 'ES' for Severely sensitive")
        moisture = str(input('YOUR RESPONSE: '))
        inp1.at[i, 'Moisture'] = moisture
elif res in ['N', 'n']:
#MSD will be applied only to the immediate roof
    for i in range(0, NOU):
        if i == 0:
            print('What is the Moisture Sensitivity of the structural unit that forms the immediate roof?')
            print("Enter 'NS' for Not sensitive, 'SS' for Slightly sensitive,")
            print("'MS' for Moderate sensitive, 'ES' for Severely sensitive")
            moisture = str(input('YOUR RESPONSE: '))
            inp1.at[i, 'Moisture'] = moisture
        else:
            moisture ='N/A'
            inp1.at[i, 'Moisture'] = moisture

#----------Generate Input 1---------
writer = pd.ExcelWriter('CMRR-Input1.xlsx', engine='xlsxwriter')
inp1.to_excel(writer, index=False, columns=['Unit','Start Depth','End Depth','Thickness','UCS','DPLT','RQD','FS','Moisture'])
writer.save()
print("CMRR-Input1.xlsx has been generated.")