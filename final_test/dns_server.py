# import libraries
import ipaddress
from scapy.all import *
import socket
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import UDP, IP

# constants
IP_LISTEN = "0.0.0.0"
PORT = 8153
SOCKET_TIMEOUT = 10
DNS_SERVER = '8.8.8.8'
DNS_TYPE_A = 'A'
DNS_TYPE_PTR = 'PTR'
SPORT = 55555
D_PORT = 53
TIMEOUT = 10
HTTP_ERROR = "HTTP/1.0 500 Internal Server Error\r\n\r\n"
HTTP_OK = "HTTP/1.0 200 OK\r\n"
HTTP_NOT_FOUND = "HTTP/1.0 404 Not Found\r\n\r\n"


# This function is checking if the address ip is valid
def validate_ip(s):
    try:
        ip = ipaddress.ip_address(s)
        if not ipaddress.ip_address(ip).is_private:
            return True
        return False
    except ValueError:
        return False


# This function create a dns request (A or PTR)
def create_request(dns, typ):
    return IP(dst=DNS_SERVER) / UDP(sport=SPORT, dport=D_PORT) / DNS(qdcount=1, rd=1) / DNSQR(qname=dns, qtype=typ)


# This function return the dns reply
def get_response(request):
    return sr1(request, verbose=0, timeout=TIMEOUT)


# This function return all the DNS RR of a specific type
def get_type(my_packet, typ):
    lst = []
    for i in range(int(my_packet[DNS].ancount)):
        if my_packet[DNSRR][i].type == 1 and typ == 1:
            lst += [my_packet[DNSRR][i].rdata]
        if my_packet[DNSRR][i].type == 12 and typ == 12:
            lst += [my_packet[DNSRR][i].rdata.decode()]
    return lst


# This function handle the request from the client
def handle_client_request(resource, client_socket):
    request = resource[1:].split('/')

    # type A
    if len(request) == 1:
        print("Type A request")
        # create and send the dns packet
        dns_request = create_request(request[0], DNS_TYPE_A)
        response_packet = get_response(dns_request)

        # check if we didn't got an answer
        if response_packet is None:
            http_response = HTTP_NOT_FOUND.encode()
        else:
            # create the HTTP reply
            list_A = get_type(response_packet, 1)
            http_header = HTTP_OK + "Content-Type: text/html; charset=utf-8\r\n"
            data = "Content-Length: " + str(len('<br>'.join(list_A))) + "\r\n\r\n" + '<br>'.join(list_A)
            http_response = (http_header + data).encode()

        # sending the response
        client_socket.send(http_response)

    # type PTR
    elif len(request) == 2 and request[0] == "reverse":
        print("Type PTR request")

        # checking if the ip is valid
        if not validate_ip(request[1]):
            http_response = HTTP_NOT_FOUND.encode()
            client_socket.send(http_response)
            return

        # create and send the dns packet
        dns_domain = request[1].split('.')
        dns_domain.reverse()
        dns_domain = ('.'.join(dns_domain)) + ".in-addr.arpa"
        dns_request = create_request(dns_domain, DNS_TYPE_PTR)
        response_packet = get_response(dns_request)

        # check if we didn't got an answer
        if response_packet is None:
            http_response = HTTP_NOT_FOUND.encode()
        else:
            # create the HTTP reply
            list_A = get_type(response_packet, 12)
            http_header = HTTP_OK + "Content-Type: text/html; charset=utf-8\r\n"
            data = "Content-Length: " + str(len('<br>'.join(list_A))) + "\r\n\r\n" + '<br>'.join(list_A)
            http_response = (http_header + data).encode()

        # sending the response
        client_socket.send(http_response)

    # we didn't got an dns type A/PTR request
    else:
        http_response = HTTP_NOT_FOUND.encode()
        client_socket.send(http_response)


# This function is checking if the HTTP request is valid
def validate_dns_request(request):
    html_request = request.split("\r\n")
    html_request = html_request[0].split(" ")
    if len(html_request) == 3:
        if html_request[0] == "GET" and html_request[2] == "HTTP/1.1":
            return True, html_request[1]
        else:
            return False, ""
    else:
        return False, ""


# This func handle the client
def handle_client(client_socket):
    print('Client connected')
    while True:
        client_request = client_socket.recv(1024).decode()
        valid_http, resource = validate_dns_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            http_header = HTTP_ERROR
            client_socket.send(http_header.encode())
            break
    print('Closing connection')
    client_socket.close()


def main():
    # creating the socket and listening
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP_LISTEN, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    # user connected
    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        try:
            handle_client(client_socket)
        except socket.timeout:
            print("timeout")


if __name__ == '__main__':
    main()
