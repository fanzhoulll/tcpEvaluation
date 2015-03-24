#Change random seed
global defaultRNG
$defaultRNG seed 0

#Create a simulator object
set ns [new Simulator]

#Default Protocol
set arg0 Tahoe
#Default CBR rate
set arg1 1 

#Read arguments
if {$argc == 2} {
	set arg0 [expr [lindex $argv 0]]
	set arg1 [expr [lindex $argv 1]]
}

#Set simulation environment
set fastLink 100Mb
set slowLink 1Mb
set shortDelay 5ms
set longDelay 40ms
set qSize [expr {125}]
set flowTime 50.0
set runTime 60.0

#Parameter for TCP
set overhead 0

#Parameter for UDP
set cbrRate $arg1
append cbrRate mb

#Open the nam file basic1.nam and the variable-trace file basic1.trace
set nf [open tcpEvaluation.nam w]
$ns namtrace-all $nf
set prefix ./trFiles/
append prefix $arg0
append prefix _
append prefix $arg1
append prefix Mbps
set tf [open $prefix w]
$ns trace-all $tf

#Define a 'finish' procedure
proc finish {} {
        global ns nf tf
        $ns flush-trace	
        close $nf		
        close $tf
        exit 0
}

#Create the network nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]

#Create a duplex link between the nodes

$ns duplex-link $n0 $n1 $fastLink $shortDelay DropTail
$ns duplex-link $n4 $n1 $fastLink $shortDelay DropTail
$ns duplex-link $n1 $n2 $fastLink $longDelay DropTail
$ns duplex-link $n2 $n3 $fastLink $shortDelay DropTail
$ns duplex-link $n2 $n5 $fastLink $shortDelay DropTail

# The queue size at $n1-n2 is to be 7, including the packet being sent
$ns queue-limit $n1 $n2 $qSize
 
# Set error model
set lossModel [new ErrorModel]
$lossModel unit pkt
$lossModel set rate_ 0.001
$lossModel ranvar [new RandomVariable/Uniform]
#$ns lossmodel $lossModel $n1 $n2

# some hints for nam
# color packets of flow 0 red
$ns color 0 Red	
$ns color 1 Blue
			
$ns duplex-link-op $n0 $n1 orient right-down
$ns duplex-link-op $n4 $n1 orient right-up
$ns duplex-link-op $n1 $n2 orient right
$ns duplex-link-op $n2 $n3 orient right-up
$ns duplex-link-op $n2 $n5 orient right-down

#Monitor the queue for link (n2-n3). (for NAM)
#$ns duplex-link-op $n1 $n2 queuePos 0.5

# Create a TCP sending agent and attach it to A
if ([string equal $arg0 Newreno]) {
	set tcp0 [new Agent/TCP/Newreno]
} else {
	set tcp0 [new Agent/TCP/Linux]
	set select_tcp "$tcp0 select_ca "
	append select_tcp $arg0
	$ns at 0 $select_tcp
}


$tcp0 set fid_ 0
$tcp0 set window_ 10000
if ([string equal $arg0 Vegas]) {
	$tcp0 set packetSize_ 1000
} else {
	$tcp0 set packetSize_ 960
}
$tcp0 set overhead_ $overhead
$ns attach-agent $n0 $tcp0

# Let's trace some variables
$tcp0 attach $tf
$tcp0 tracevar cwnd_
$tcp0 tracevar ssthresh_
$tcp0 tracevar ack_
$tcp0 tracevar maxseq_

#Create a TCP receive agent (a traffic sink) and attach it to n4
set end0 [new Agent/TCPSink/Sack1]
$ns attach-agent $n3 $end0
$ns connect $tcp0 $end0  

#Schedule the tcp data flow; start sending data at T=0, stop at T=10.0
set myftp [new Application/FTP]
$myftp attach-agent $tcp0

#Setup a UDP connection
set udp [new Agent/UDP]
$udp set fid_ 1
$ns attach-agent $n4 $udp

#Create a UDP receive agent (a traffic sink) and attach it to n6
set end1 [new Agent/Null]
$ns attach-agent $n5 $end1
$ns connect $udp $end1

# Set a CBR flow over it
set mycbr [new Application/Traffic/CBR]
$mycbr set type_ CBR
$mycbr set packet_size_ 1000
$mycbr set rate_ $cbrRate
$mycbr set random_ 1
$mycbr attach-agent $udp

#Schedule events for the CBR and FTP agents
$ns at 0.0 "$mycbr start"
$ns at 0.0 "$myftp start"
$ns at $flowTime "$myftp stop"
$ns at $flowTime "$mycbr stop"
$ns at $runTime "finish"

#Run the simulation
$ns run
