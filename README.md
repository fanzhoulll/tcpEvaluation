# TCP evaluation

[Project website](http://david.choffnes.com/classes/cs4700sp15/project3.php)


Introduction
===========
In this paper, we will  the performance of different TCP protocols and how these performance are 
influenced by varying networking environment. We are mainly interested in 4 problems:

1. What is the overall performance (throughput, delay, etc) of single TCP flow?
2. What is the fairness between two TCP flows?
3. How will the queue management discipline influence the performance of TCP?
4. What is the limitation of traditional TCP and what are possible solutions?

To answer these problems, many experiments are conducted. All experiments are done in NS2, which used to be the
most popular network simulation tool. Every experiment will be run for 100 
seconds and at least 32 times to guarantee statistical significance. 

Next we will briefly introduce the experiments methodology. For detailed description please refer to full paper. 

Simulation environment
======================

1. Traffic
----------
Here we use the simplest bulk sending model. The senders always have data to send. We inject new packets in the sending bufferas long as it is empty. We use this model to study the performance of protocols while the bottleneck link is always busy. 

2. Topology
-----------
We use the simple dumbbell network. The topology is shown in the following figure:
<pre>
                         N1                      N4
                           \                    /
                            \                  /
                             N2--------------N3
                            /                  \
                           /                    \
                         N5                      N6
</pre>
The bandwidth of all links are 10Mbps. The link between N2 and N3 is bottleneck link. We will add a constant bit rate flow between N2 and N3. By varying the bit rate of this CBR flow, we can simulate the TCP’s performance under congestion. 

3. End-to-End latency
------------------
We assume that the link delay between N2 to N3 is 40ms and the link delay for all the other link is 5ms. This assumption is to simulate the performance of bottleneck link. The round trip time between N1 to N4 (or from N5 to N6) is therefore 100ms.

4. Queue buffer
------------------
Due to the limiation of length, we are not going to study the influence of varying queue buffer in this report (though it is very important). We would set the queue buffer to be 1 BDP (bandwidth delay product).

Experiments methologies
======================

###Experiment 1: TCP Performance Under Congestion
In this experiment, we study the performance of single TCP flow under congestion. Four different TCP flavours are studied in this experiment: Tahoe, Reno, NewReno and Vegas. Here we does not change the bandwidth of bottleneck link bandwidth, instead, we add a CBR flow between N2 and N3 to change the available bandwidth for TCP flow. The varying parameters and  performance metrics are listed in following table (for each TCP mentioned above):

Available Bandwidth  | Throughput | Link utilization | Average Latency | Packet drop rate
-------------------- | ---------- | ---------------- | --------------- | --------------- |
2Mbps  | | | | 
4Mbps  | | | | 
8Mbps  | | | | 

Following questions will be answered:

1. Which TCP variant(s) are able to get higher average throughput? 
2. Which achieves the highest link utilization? 
3. Which has the lowest average latency? 
4. Which has the fewest drops? 
5. Is there an overall "best" TCP variant in this experiment, or does the "best" variant vary depending on other circumstances?

###Experiment 2: Fairness Between TCP Variants

In this experiment, we study the fairness between different TCP flows. We use Jain's index to measure fairness. The equation is as followings:

f = (x1+x2+..xn)^2/n*(x1^2+x2^2+....xn^2)

f is the fairness index, xi is the throughput of i’th flow. Notice that fairness itself is a very complex topic. Here we only study protocol-fairness, i.e, compare the fairness between different protocols (Reno/Reno, NewReno/Reno, Vegas/Vegas,NewReno/Vegas) with the same RTT. The parameters and performance metrics we are going to measure are listed as followings:

Available Bandwidth  | Fairness index 
-------------------- | --------------|
2Mbps  |  
4Mbps  |  
8Mbps  | 

The fairness index can only gives us very limit information. We are more interested in the dynamics of one TCP flow after another TCP flow joins. So more experiments will be done. For example we will plot real time throughput of two TCP flows with different starting time. An sample would be like:

Protocol/Protocol  | Start time for flow 1 | Start time for flow 2  
------------------ | --------------------- | --------------------|
NewReno/Vegas      |  0 | 5s 

The questions to be answered are:

1. Are the different combinations of variants fair to each other? 
2. Are there combinations that are unfair, and if so, why is the combination unfair? 

###Experiment 3: Influence of Queuing
The queuing discipline has significant impact to the performance of TCP. In this experiment, we will study two queuing methods: drop tail and random early detection. Two protocols used are Reno and SACK. We start the first TCP flow, then add another CBR flow (fixed bandwidth). Real time performance in terms of throughput and delay will be plotted for the TCP flow. As stated above, we are not going to do the simulation with varying queue buffer and will simply assume it to be 1 BDP.

We are going to answer following questions:

1. Does each queuing discipline provide fair bandwidth to each flow?
2. How does the end-to-end latency for the flows differ between DropTail and RED?
3. How does the TCP flow react to the creation of the CBR flow?
4. Is RED a good idea while dealing with SACK?

###Experiment 4: Limitation of traditional TCP and solutions

It has long been known that classical TCP protocols (Tahoe, Reno, NewReno) perform bad in lossy or high BDP network. In this experiment we will pick NewReno as the representation of classical TCP protocol and compare it with new variations of TCP in more challenging network conditions. The protocols are are going to study in this experiments are NewReno, Westwood+, and Cubic. Westwood+ is famous for its ability to fast recovery from non-congestion packet loss. Cubic is the default TCP protocol for Linux system and is known as its great performance in high BDP network. 

First we study the performance of TCP NewReno and TCP Westwood+ with lossy link (like wireless network).

Protocol: NewReno/Westwood+

Packet loss rate  | Throughput | Link utilization | Average Latency
------------------| ---------- | ---------------- | ---------------| 
1*10^(-6)  | | |  
5*10^(-6)  | | | 
1*10^(-5)  | | |  
5*10^(-5)  | | |
1*10^(-4)  | | |

Next we study the performance of TCP NewReno and TCP Cubic in high BDP network. Notice in this experiments we only care the bottleneck bandwidth. We can set the bandwidth of other links to an arbitrarily high value, like 100 Mbps. Also, we assume the bottleneck buffer is always 1 BDP. 

Protocol: NewReno/Cubic

Available Bandwidth  | Throughput | Link utilization | Average Latency | Packet drop rate
-------------------- | ---------- | ---------------- | --------------- | --------------- |
10Mbps  | | | | 
15Mbps  | | | | 
20Mbps  | | | | 
25Mbps  | | | |
30Mbps  | | | |

After this experiment, we hope two following questions could be answered:

1. What are the problems faced by classical TCP’s performance and how new TCP varients try to solve them?
2. Can we further improve the performance of TCP?

Reproducing the Results
=======================

To be added...
