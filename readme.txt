###############################################################################################

This repository consists of the scripts related to my Master-Thesis.

The main focus of the thesis is to design and implement Concurrent Multipath Transmission which is an extension of SCTP in real-time.
Generally, only one network is made active at a time even if multiple connections are present for a system. For this thesis 3 networks are used at the client and one at the server. Hence, certain modifications are to be made at the client side before transmitting the data.  

1) Run script "network-setup.sh" modifying the network addresses that are available.
2) "client.py" and "server.py" must be run at the source and the destination simultaneously for transmitting and recieving the data.
