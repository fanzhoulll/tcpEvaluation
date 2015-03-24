#!/usr/bin/python2

#Calculate cwnd, throughput, queue, RTT
#Show average throughput of each flow

from __future__ import division
import nstrace
import sys
import os
import matplotlib.pyplot as plt

N0 = 0
N1 = 1
N2 = 2
N3 = 3
N4 = 4
N5 = 5
N6 = 6
BANDWIDTH = 10 # Mbps
Pkt_Size = 1000 # Byte

def draw(filename, xAxis, yAxis):
   #fullPath = os.getcwd() + "/" + filename
   drawFile = open("./Statistic/" + filename, 'r')
   time = []
   value = []
   for line in drawFile:
      columns = line.split()
      time.append(columns[0])
      value.append(columns[1])
   plt.plot(time, value)
   plt.xlabel(xAxis)
   plt.ylabel(yAxis)

def isVar(theLine):
   return len(theLine.split()) == 7

def isEvent(theLine):
   return len(theLine.split()) == 12

def getVar(theLine):
   splitLine = theLine.split()
   tuple = (
            float(splitLine[0]),	# time
            int(splitLine[1]),		# source node
	    int(splitLine[2]),		# source flowid
	    int(splitLine[3]),		# dest node
	    int(splitLine[4]),		# dest flowid
	    splitLine[5],			# name of traced var
	    float(splitLine[6])		# value
	    )
   return tuple

# pair() takes a string of the form "n.m" and converts it to a tuple (n m)
def pair(str):
   list = str.split(".")
   return (int(list[0]), int(list[1]))
      
def getEvent(theLine):
   splitLine = theLine.split()
   tuple = (
         splitLine[0],			# "r", "d", "+", "-"
         float(splitLine[1]),		# time
         int(splitLine[2]),		# sending node
         int(splitLine[3]),		# dest node
         splitLine[4],			# protocol
         int(splitLine[5]),		# size
         splitLine[6],			# flags
         int(splitLine[7]),		# flow ID
         pair(splitLine[8]),		# source (node flowid)
         pair(splitLine[9]),		# dest (node flowid)
         int(splitLine[10]),		# seq #
         int(splitLine[11])		# packet ID
         )
   return tuple

def record_results(filename, flowID, averageThroughput, averageRTT, drop_count, sent_count):
   result_file_name = filename + "_" + str(flowID)
   result_file = open("./Results/" + result_file_name, 'a')
   drop_rate = round(drop_count/sent_count, 4)
   line = str(averageThroughput) + " " + str(averageRTT) + " " + str(drop_rate) + " " + str(drop_count) + " " + str(sent_count)
   result_file.write(line + "\n")
   result_file.close()
   print (filename + " && Flow " + str(flowID))
   #print ("Average throughput: " + str(averageThroughput) + "Mbps")
   print ("Average delay: " + str(averageRTT) + "s")
   #print ("packet drop: "  + str(drop_count))
   #print ("packet sent: " + str(sent_count))
   #print ("drop rate: " + str(round(drop_count/sent_count, 4)))
   #print ("\n")

def calculate_All(flowID):
   rootPath = './trFiles'
   for trFile in os.listdir(rootPath):
      trFilePath = os.path.join(rootPath, trFile)
      calculate(trFilePath, flowID)
   #print ("\n")

def calculate(trFilePath, flowID):
   trFile = open(trFilePath, 'r')
   trFileName = trFilePath.split("/")[-1]
   FLOW = flowID
   INTERVAL = 0.5 # The time interval to calculate throughput
   STARTPOINT = 0 # In case want to wait until slow start is done
   STARTPOINT_drop = 2 # We can only do drop calculating after slow start is done
   lastTime = 0 # For calculate throughput
   intervalData = 0 # For calculate throughput
   totalDate = 0 # For calculate throughput
   SHORTDELAY = 0.005 # For calculate RTT
   LONGDELAY = 0.04 # For calculate RTT
   BASERTT = (LONGDELAY + 2 * SHORTDELAY) * 2 # For calculate RTT
   totalDelay = 0 # For calculate average RTT
   delayCount = 0 # For calculate average RTT
   lastEnqueueTime = 0 # For calculate Queue
   queueSize = 0 # For calculate Queue
   drop_count = 0 # For calculating drop rate
   sent_count = 0 # For calculating drop rate
   cwnd_file_name = 'cwnd_' + str(flowID)
   throughput_file_name = 'throughput_' + str(flowID)
   rtt_file_name = 'RTT_' + str(flowID)
   queue_file_name = 'queue'
   cwnd_file = open("./Statistic/" + cwnd_file_name,'w')
   throughput_file = open("./Statistic/" + throughput_file_name,'w')
   rtt_file = open("./Statistic/" + rtt_file_name,'w')
   queue_file = open("./Statistic/" + queue_file_name,'w')
   for line in trFile:
      if isVar(line):
         (time, snode, dummy, dummy, flow, varname, cwnd) = getVar(line)
         if (time >= STARTPOINT and varname == "cwnd_"):
            if ((FLOW == 0 and snode == N0) or (FLOW == 1 and snode == N4)):
               cwnd_file.write(str(time) + " " + str(cwnd) + "\n")
      elif isEvent(line):
         (event, time, sendnode, dest, dummy, size, dummy, flow, dummy, dummy, dummy, packetID) = getEvent(line)
         if (sendnode == N1 and dest == N2 and size >= 1000):
            if (event == "+"):
               queueSize += 1
               lastEnqueueTime = time
               queue_file.write(str(time) + " " + str(queueSize) + "\n")
            elif (event == "-"):
               queueSize -= 1
               queue_file.write(str(time) + " " + str(queueSize) + "\n")
            elif (event == "d"):
               if (time == lastEnqueueTime):
                  queueSize -= 1
               queue_file.write(str(time) + " " + str(queueSize) + "\n")
            if (flow == FLOW):
               if (event == "r"): # Calculate throughput
                  if (STARTPOINT == 0):
                     STARTPOINT = time
                  if (time < lastTime + INTERVAL):
                     intervalData += size
                     totalDate += size
                  else:
                     intervalThroughput = 8*intervalData/(1000000*(time - lastTime))
                     time = round(time, 2)
                     intervalThroughput = round(intervalThroughput, 2)
                     if(time > STARTPOINT):
                        throughput_file.write(str(time) + " " + str(intervalThroughput) + "\n")
                     lastTime = time
                     intervalData = size
                     totalDate += size
               elif (event == "+"): # Calculate RTT 
                  time = round(time, 2)
                  queueDelay = queueSize*Pkt_Size*8/(BANDWIDTH*1000000)
                  RTT = round(BASERTT + queueDelay, 4)
                  totalDelay += RTT
                  delayCount += 1
                  if(time > STARTPOINT):
                     rtt_file.write(str(time) + " " + str(RTT) + "\n")
               elif (event == "-"): # Calculate RTT and drop rate
                  sent_count += 1
                  time = round(time, 2)
                  queueDelay = queueSize*Pkt_Size*8/(BANDWIDTH*1000000)
                  RTT = round(BASERTT + queueDelay, 4)
                  totalDelay += RTT
                  delayCount += 1
                  if(time > STARTPOINT):
                     rtt_file.write(str(time) + " " + str(RTT) + "\n")
               elif (event == "d"): # Calculate RTT and drop rate
                  #time = round(time, 2)
                  queueDelay = queueSize*Pkt_Size*8/(BANDWIDTH*1000000)
                  RTT = round(BASERTT + queueDelay, 4)
                  totalDelay += RTT
                  delayCount += 1
                  if(time > STARTPOINT):
                     rtt_file.write(str(time) + " " + str(RTT) + "\n")
                  if(time > STARTPOINT_drop):
                     drop_count += 1
   # Enough reading and writing. Close all files
   trFile.close()
   cwnd_file.close()
   throughput_file.close()
   queue_file.close()
   rtt_file.close()
   # Calculate average throughput, delay
   averageThroughput = 8*totalDate/(1000000*(lastTime - STARTPOINT))
   #print (lastTime, totalDate)
   averageThroughput = round(averageThroughput, 2)
   averageRTT = round(totalDelay/delayCount, 4)
   # Handle all the results
   record_results(trFileName, FLOW, averageThroughput, averageRTT, drop_count, sent_count)
   # Draw everything
   #plt.figure(1)
   #draw(cwnd_file_name, 'time', 'cwnd')
   #plt.figure(2)
   #draw(throughput_file_name, 'time', 'Throughput')
   #plt.figure(3)
   #draw(rtt_file_name, 'time', 'rtt')
   #plt.figure(4)
   #draw(queue_file_name, 'time', 'queue')
   #plt.show()

calculate_All(0)
calculate_All(1)
