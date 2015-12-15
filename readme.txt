This Master Thesis is to design and implement CMT (Concurrent Multipath Transmission) which is an extension of standard transport layer protocol, SCTP.

In general, a system has only one active network even though there are many networks available at a time. To make number of networks active some Linux Kernel configurations are to be modified. Here, 3 networks are used at the client and 2 at the destination.

1) Run the script "network-setup.sh" (by changing the network addresses that are available) which is an automated code to modify the configurations. 
2) Run scripts "client.py" and "server.py" simultaneously at source and destination respectively. 

For more information, refer "Thesis Report.pdf".
