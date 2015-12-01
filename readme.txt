# Master-Thesis

This Master-Thesis is to design and implement CMT (Concurrent Multipath Transmission) which is an extension of standard transport layer protocol, SCTP.

In general, a system has only one active network even though there are many networks available at a time. To make number of networks active some linux kernel configurations are to be modified. Here, 3 networks are used at the client side and only one at the destination.

Run the script "network-setup.sh" which is an automated code to modify the configurations. Run scripts "client.py" and "server.py" simultaneously at source and destination respectively. 
