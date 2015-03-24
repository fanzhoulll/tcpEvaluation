import os
import statistic

def doExperiment1(times):
    count = 0
    while (count < times):
        protocols = ['Tahoe', 'Reno', 'Newreno', 'Vegas']
        print ("This is " + str(count+1) + "'s " + "simulation")
        for protocol in protocols:
            for i in range(1, 10, 1):
                bandwidth = i
                cmd = 'ns experiment1.tcl ' + "{" + protocol + "}" + " " + str(bandwidth)
                #print (cmd)
                output = os.popen(cmd)
        statistic.calculate_All(0)
        count = count + 1

def doExperiment2(times):
    count = 0
    while (count < times):
        protocol_pair1 = ('Reno','Reno')
        protocol_pair2 = ('Newreno','Reno')
        protocol_pair3 = ('Vegas','Vegas')
        protocol_pair4 = ('Newreno','Vegas')
        protocols = [protocol_pair1, protocol_pair2, protocol_pair3, protocol_pair4]
        print ("This is " + str(count+1) + "'s " + "simulation")
        for protocol_pair in protocols:
            for i in range(1, 10, 1):
                bandwidth = i
                protocol1 = protocol_pair[0]
                protocol2 = protocol_pair[1]
                cmd = 'ns experiment2.tcl ' + "{" + protocol1 + "}" + " " + "{" + protocol2 + "}" + " " + str(bandwidth) 
                output = os.popen(cmd)
        statistic.calculate_All(0)
        statistic.calculate_All(1)
        count = count + 1

def doExperiment3(times):
    count = 0
    while (count < times):
        protocol_pair1 = ('Reno','DropTail')
        protocol_pair2 = ('Reno','RED')
        protocol_pair3 = ('Sack1','DropTail')
        protocol_pair4 = ('Sack1','RED')
        protocols = [protocol_pair1, protocol_pair2, protocol_pair3, protocol_pair4]
        print ("This is " + str(count+1) + "'s " + "simulation")
        for protocol_pair in protocols:
            for i in range(1, 3, 1):
                bandwidth = i
                protocol1 = protocol_pair[0]
                protocol2 = protocol_pair[1]
                cmd = 'ns experiment3.tcl ' + "{" + protocol1 + "}" + " " + "{" + protocol2 + "}" + " " + str(bandwidth) 
                output = os.popen(cmd)
        statistic.calculate_All(0)
        statistic.calculate_All(1)
        count = count + 1
        
def doExperiment4_1(times):
    count = 0
    while (count < times):
        protocols = ['Newreno', 'westwood']
        print ("This is " + str(count+1) + "'s " + "simulation")
        for protocol in protocols:
            for i in range(2, 8, 1):
                lossIndex = i
                cmd = 'ns experiment4_1.tcl ' + "{" + protocol + "}" + " " + str(lossIndex) 
                output = os.popen(cmd)
        statistic.calculate_All(0)
        count = count + 1

def doExperiment4_2(times):
    count = 0
    while (count < times):
        protocols = ['Newreno', 'cubic']
        print ("This is " + str(count+1) + "'s " + "simulation")
        for protocol in protocols:
            for i in range(10, 100, 10):
                bandwidth = i
                cmd = 'ns experiment4_2.tcl ' + "{" + protocol + "}" + " " + str(bandwidth) 
                output = os.popen(cmd)
        statistic.calculate_All(0)
        count = count + 1
        
#doExperiment1(100)
#doExperiment2(100)
#doExperiment3(2)
#doExperiment4_1(100)
doExperiment4_2(7)
