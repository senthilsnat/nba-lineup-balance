import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from radar import radar_graph
from radar import stacked_radar

# import and look at centers data
with open("allplayers percentile ver lineup filtered.csv", 'r') as myFile:
    dataLines = myFile.read().splitlines()

data_temp = []
for z in range(1, len(dataLines)):
    data_temp.append(dataLines[z].split(','))

print data_temp

data = []
for i in range(len(data_temp)):
    temp = []
    for j in range(3, len(data_temp[0])):
        if data_temp[i][j] == '':
            temp.append(0)
        else:
            temp.append(float(data_temp[i][j]))
    temp.append(str(data_temp[i][0]))
    temp.append(str(data_temp[i][1]))

data.append(temp)

print data

# prepare data for feeding into radar chart
label = dataLines[0].split(',')
label.remove('Player')
label.remove('Tm')
label.remove('MP')
print label

cases = []
legend_names = []
graph_name = ''

# uncomment below block to run quick tests on one lineup at a time
'''
    summer = 0
    for n in data[65:70]:
    print n
    ind = data.index(n)
    graph_name = "Bogut Mavs"
    name = n[-2]
    legend_names.append(n[-2])
    cases.append(n[:-2])
    summer += sum(n[:-2])
    
    stacked_radar(graph_name, label, legend_names, cases[0], cases[1], cases[2], cases[3], cases[4])
    print "balance :", round(100*(summer/(100*17*5)))  # correct ver
    '''

count = 0
summer = 0
for n in data:
    ind = data.index(n)
    
    # prepare labels on radar chart
    graph_name = n[-1]
    name = n[-2]
    legend_names.append(n[-2])
    cases.append(n[:-2])
    summer += sum(n[:-2])
    count += 1
    # iterate through csv file in intervals of 5 (one lineup at a time)
    if (count % 5) == 0:
        count = 0
        # print radar chart
        stacked_radar(graph_name, label, legend_names, cases[0], cases[1], cases[2], cases[3], cases[4])
        print graph_name, ":", round(100.0*(summer/(100*17*5))), "%"
        
        # area of a heptadecagon (17 sides) with circumradius 100 is 30705.5
        # area of a heptadecagon (17 sides) with circumradius 500 (in a stacked radar) is ~767639
        
        # Previously incorrect version of this calculation used the area of a filled radar..
        # This was a misrepresentative and inaccurate understanding of the inconsistencies with radar charts
        # Updated calculation is simpler and better represents how much of the maximum is achieved in a given lineup
        
        summer = 0
    
    # reset iteration variables to prepare for next radar chart
    if ((ind+1) % 5) == 0:
        cases = []
        legend_names = []
        graph_name = ''
