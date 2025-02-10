#!/bin/sh
#
# A shell script used to setup rules for iptables.  Rules gleened from 
# various websites.
# 
# References:
#  http://www.newartisans.com/blog_files/tricks.with.iptables.php

# Wipe the tables clean
iptables -F


# INPUT SIDE
# Accept all loopback input
iptables -A INPUT -i lo -p all -j ACCEPT

# Allow the three way handshake
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
 
# Reject spoofed packets
iptables -A INPUT -s 10.0.0.0/8 -j DROP 
iptables -A INPUT -s 169.254.0.0/16 -j DROP
iptables -A INPUT -s 172.16.0.0/12 -j DROP
iptables -A INPUT -s 127.0.0.0/8 -j DROP

iptables -A INPUT -s 224.0.0.0/4 -j DROP
iptables -A INPUT -d 224.0.0.0/4 -j DROP
iptables -A INPUT -s 240.0.0.0/5 -j DROP
iptables -A INPUT -d 240.0.0.0/5 -j DROP
iptables -A INPUT -s 0.0.0.0/8 -j DROP
iptables -A INPUT -d 0.0.0.0/8 -j DROP
iptables -A INPUT -d 239.255.255.0/24 -j DROP
iptables -A INPUT -d 255.255.255.255 -j DROP
 
# Stop smurf attacks
iptables -A INPUT -p icmp -m icmp --icmp-type address-mask-request -j DROP
iptables -A INPUT -p icmp -m icmp --icmp-type timestamp-request -j DROP
iptables -A INPUT -p icmp -m icmp -m limit --limit 1/second -j ACCEPT
 
# Drop all invalid packets
iptables -A INPUT -m state --state INVALID -j DROP
iptables -A FORWARD -m state --state INVALID -j DROP
iptables -A OUTPUT -m state --state INVALID -j DROP

# Drop excessive RST packets to avoid smurf attacks
iptables -A INPUT -p tcp -m tcp --tcp-flags RST RST -m limit --limit 2/second --limit-burst 2 -j ACCEPT

# Attempt to block portscans
# Anyone who tried to portscan us is locked out for an entire day.
iptables -A INPUT   -m recent --name portscan --rcheck --seconds 86400 -j DROP
iptables -A FORWARD -m recent --name portscan --rcheck --seconds 86400 -j DROP

# Once the day has passed, remove them from the portscan list
iptables -A INPUT   -m recent --name portscan --remove
iptables -A FORWARD -m recent --name portscan --remove

# These rules add scanners to the portscan list, and log the attempt.
iptables -A INPUT   -p tcp -m tcp --dport 139 -m recent --name portscan --set -j LOG --log-prefix "Portscan:"
iptables -A INPUT   -p tcp -m tcp --dport 139 -m recent --name portscan --set -j DROP

iptables -A FORWARD -p tcp -m tcp --dport 139 -m recent --name portscan --set -j LOG --log-prefix "Portscan:"
iptables -A FORWARD -p tcp -m tcp --dport 139 -m recent --name portscan --set -j DROP

# Allow the following ports through from outside
# smtp
iptables -A INPUT -p tcp -m tcp --dport 25 -j ACCEPT
# http 
iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
# pop3 
iptables -A INPUT -p tcp -m tcp --dport 110 -j ACCEPT
# imap
iptables -A INPUT -p tcp -m tcp --dport 143 -j ACCEPT
# https
iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
# imaps
iptables -A INPUT -p tcp -m tcp --dport 993 -j ACCEPT
# pop3s
iptables -A INPUT -p tcp -m tcp --dport 995 -j ACCEPT
# ssh & sftp
iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
# ntpdate
iptables -A INPUT -p udp -m udp --dport 123 -j ACCEPT
# mysql
iptables -A INPUT -p tcp -m tcp --dport 3306 -j ACCEPT

# Allow pings through
iptables -A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

# Kill all other input 
iptables -A INPUT -j REJECT


# Output side
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow the following ports through from outside
# smtp
iptables -A OUTPUT -p tcp -m tcp --dport 25 -j ACCEPT
# DNS requests
iptables -A OUTPUT -p udp -m udp --dport 53 -j ACCEPT
# DHCP/Bootstrap Protocol Server
iptables -A OUTPUT -p udp -m udp --dport 67 -j ACCEPT
# http 
iptables -A OUTPUT -p tcp -m tcp --dport 80 -j ACCEPT
# pop3 
iptables -A OUTPUT -p tcp -m tcp --dport 110 -j ACCEPT
# imap
iptables -A OUTPUT -p tcp -m tcp --dport 143 -j ACCEPT
# https
iptables -A OUTPUT -p tcp -m tcp --dport 443 -j ACCEPT
# imaps
iptables -A OUTPUT -p tcp -m tcp --dport 993 -j ACCEPT
# pop3s
iptables -A OUTPUT -p tcp -m tcp --dport 995 -j ACCEPT
# ssh & sftp
iptables -A OUTPUT -p tcp -m tcp --dport 22 -j ACCEPT
# ntpdate
iptables -A OUTPUT -p udp -m udp --dport 123 -j ACCEPT
# mysql
iptables -A OUTPUT -p tcp -m tcp --dport 3306 -j ACCEPT

# Allout pings out
iptables -A OUTPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

# Kill all other output
iptables -A OUTPUT -j REJECT


# FORWARD SIDE
iptables -A FORWARD -j REJECT

# Save
service iptables save

# Restart
service iptables restart