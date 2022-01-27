import ipaddress
import sys
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import UDP, IP
from scapy.sendrecv import sr1

DNS_SERVER = '8.8.8.8'
DNS_TYPE_A = 'A'
DNS_TYPE_PTR = 'PTR'
SPORT = 55555
DPORT = 53
TIMEOUT = 2


# checking if ip is valid and public
def validate_ip(s):
    try:
        ip = ipaddress.ip_address(s)
        if not ipaddress.ip_address(ip).is_private:
            return True
        return False
    except ValueError:
        return False


# checking if ip is valid
def is_ip(s):
    try:
        ip = ipaddress.ip_address(s)
        return True
    except ValueError:
        return False


def get_type(packet, typ):
    lst = []
    for i in range(int(packet[DNS].ancount)):
        if packet[DNSRR][i].type == typ:
            lst += [packet[DNSRR][i].rdata]
    return lst


def create_request(dns, typ):
    return IP(dst=DNS_SERVER) / UDP(sport=SPORT, dport=DPORT) / DNS(qdcount=1, rd=1) / DNSQR(qname=dns,qtype=typ)


def get_response(request):
    return sr1(request, verbose=0, timeout=TIMEOUT)


def main():
    # checking the passed arguments
    if len(sys.argv) == 2 and not is_ip(sys.argv[1]):
        type_req = DNS_TYPE_A
        dns_domain = sys.argv[1]
    elif len(sys.argv) == 3 and sys.argv[1] == '-type=PTR' and validate_ip(sys.argv[2]):
        type_req = DNS_TYPE_PTR
        dns_domain = sys.argv[2].split('.')
        dns_domain.reverse()
        dns_domain = ('.'.join(dns_domain)) + ".in-addr.arpa"
    else:
        print("ERROR")
        exit()

    # creating the dns request
    dns_request = create_request(dns_domain, type_req)
    # sending the dns request and sniff the answer
    response_packet = get_response(dns_request)

    # if timeout occur then exit
    if response_packet is None:
        print("TIMEOUT")
        exit()

    # printing the answer
    print("Name:     " + dns_domain)
    print("Addresses:")

    if get_type(response_packet, 1):
        print("     TYPE A:")
        for i in get_type(response_packet, 1):
            print("        " + i)
    if get_type(response_packet, 5):
        print("     TYPE CNAME:")
        for i in get_type(response_packet, 5):
            print("        " + i.decode())
    if get_type(response_packet, 12):
        print("     TYPE PTR:")
        for i in get_type(response_packet, 12):
            print("        " + i.decode())


if __name__ == '__main__':
    main()
