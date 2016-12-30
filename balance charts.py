import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from radar import radar_graph

# import and look at centers data
with open("allplayers percentile ver lineup filtered.csv", 'r') as myFile:
    dataLines = myFile.readlines()

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
for n in data[10:15]:
    print n
    ind = data.index(n)
    graph_name = "Overlapping Lineups - DEN"
    name = n[-2]
    legend_names.append(n[-2])
    cases.append(n[:-2])

graph_areas = radar_graph(graph_name, label, legend_names, cases[0], cases[1], cases[2], cases[3], cases[4])
print graph_areas
'''

count = 0
for n in data:
    ind = data.index(n)

    # prepare labels on radar chart
    graph_name = n[-1]
    name = n[-2]
    legend_names.append(n[-2])
    cases.append(n[:-2])

    count += 1
    # iterate through csv file in intervals of 5 (one lineup at a time)
    if (count % 5) == 0:
        count = 0
        # print radar chart
        graph_areas = radar_graph(graph_name, label, legend_names, cases[0], cases[1], cases[2], cases[3], cases[4])
        print graph_name, ":", graph_areas

        # A rough measure of "balance" is simply by calculating what percentage of the figure area
        # is totally filled in by the actual players' radar charts
        # Add all five together and take as percentage of (5*area of regular heptadecagon)
        # Essentially asking, how little white space is there, and how well is it filled in?
        # area of a heptadecagon (17 sides) with circumradius 100 is 30705.5

        hepta_area = 30705.5
        balance = int(100 * (sum(graph_areas))/(5 * hepta_area))
        print "balance :", balance

    # reset iteration variables to prepare for next radar chart
    if ((ind+1) % 5) == 0:
        cases = []
        legend_names = []
        graph_name = ''
