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

Traffic
-------
Here we use the simplest bulk sending model. The senders always have data to send. We inject new packets in the sending bufferas long as it is empty. The reason that to use this model is to study the performance of protocols while the bottleneck link is kept busy. 

Topology
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






