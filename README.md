# TCP evaluation

[Project website](http://david.choffnes.com/classes/cs4700sp15/project3.php)


Introduction
===========
In this paper, we will discuss on the performance of different TCP protocols and how these performance are 
influenced by varying networking environment. We are mainly interested in 4 problems:

1. What is the overall performance (throughput, delay, etc) of single TCP flow?
2. What is the fairness situation between two TCP flows?
3. How will the queue management discipline influence the performance of TCP?
4. What is the limitation of traditional TCP and what are possible solutions?

To answer these four problems, many experiments are conducted. All experiments are done in NS2, which is the
most popular network simulation tool developed by thousands researchers. Every experiment will be run for 100 
seconds and at least 32 times to guarantee statistical significance. Next we will briefly introduce the experiments 
methodology. For detailed description please refer to full paper. 

Simulation environment
======================

1. Traffic
-------
Here we use the simplest bulk sending model. The senders always have data to send. We inject new packets in the sending bufferas long as it is empty. The reason that to use this model is to study the performance of protocols while the bottleneck link is kept busy. 

2. Topology
--------
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

Experiments methologies
======================

###Experiment 1: TCP Performance Under Congestion
In this experiment, we study the performance of single TCP flow under congestion. Four different TCP flavours are studied in this experiment: Tahoe, Reno, NewReno and Vegas. Here we does not change the bandwidth of bottleneck link bandwidth, instead, we add a CBR flow between N2 and N3 to change the available bandwidth for TCP flow. The varying parameters and corresponding performance metrics are listed in following table (for one TCP):

Available Bandwidth  | Throughput | Link utilization | Latency | Packet drop rate
------------- | -------------
2Mbps  | Content Cell
4Mbps  | Content Cell
8Mbps  | Content Cell
