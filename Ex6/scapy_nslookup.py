import sys

from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import UDP, IP
from scapy.sendrecv import sr1

if len(sys.argv) == 2:
    type_req = 'A'
    dns_domain = sys.argv[1]
elif len(sys.argv) == 3 and sys.argv[1] == '-type=PTR':
    type_req = 'PTR'
    dns_domain = sys.argv[2] + ".in-addr.arpa"
else:
    print("ERROR")
    exit()

dns_request = IP(dst='8.8.8.8') / UDP(sport=55555, dport=53) / DNS(qdcount=1, rd=1) / DNSQR(qname=dns_domain,
                                                                                            qtype=type_req)
response_packet = sr1(dns_request)

print("Name:     " + dns_domain)
print("Addresses:")

for i in range(int(response_packet[DNS].ancount)):
    if response_packet[DNSRR][i].type == 1:
        print("     TYPE A:")
        print("          " + response_packet[DNSRR][i].rdata)
    elif response_packet[DNSRR][i].type == 5:
        print("     TYPE CNAME:")
        print("          " + response_packet[DNSRR][i].rdata.decode())
    elif response_packet[DNSRR][i].type == 12:
        print("     TYPE PTR:")
        print("          " + response_packet[DNSRR][i].rdata.decode())
