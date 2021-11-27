# Ex 4.4 - HTTP Server Shell

# TO DO: import modules
import socket
import imghdr
import os

# TO DO: set constants
DEFAULT_URL = "index.html"
REDIRECTION_DICTIONARY = {"imgs\\loading.gif": "/imgs/abstract.jpg",}
FORBIDDEN = ("imgs\\test.jpg",)
IP = "0.0.0.0"
PORT = 80
SOCKET_TIMEOUT = 2


def get_file_data(filename):
    """ Get data from file """
    file = "C:\webroot\\" + filename

    if os.path.exists(file):
        if filename not in FORBIDDEN:
            if imghdr.what(file) == "jpeg":
                read_file = open(file, 'rb')
                data = read_file.read()
                data = ("Content-Length: " + (str(len(data))) + "\r\n\r\n").encode() + data
            else:
                read_file = open(file, 'r')
                data = read_file.read()
                data = ("Content-Length: " + str(len(data)) + "\r\n\r\n" + data).encode()
            read_file.close()
            return data
        else:
            return "FORBIDDEN"
    else:
        return "NOT FOUND"


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if resource == '/':
        url = DEFAULT_URL
    else:
        url = resource[1:].replace('/', '\\')

    # TO DO: check if URL had been redirected, not available or other error code. For example:
    if url in REDIRECTION_DICTIONARY:
        # TO DO: send 302 redirection response
        http_header = "HTTP/1.0 302 Found\r\nLocation: " + REDIRECTION_DICTIONARY.get(url) + "\r\n\r\n"
        client_socket.send(http_header.encode())
        return

    # TO DO: extract requested file type from URL (html, jpg etc)
    request = url.split(".")
    filetype = request[-1]

    if filetype == 'html':
        # TO DO: generate proper HTTP header
        http_header = "HTTP/1.0 200 OK\r\n" + "Content-Type: text/html; charset=utf-8\r\n"
    # TO DO: handle all other headers
    elif filetype == 'css':
        http_header = "HTTP/1.0 200 OK\r\n" + "Content-Type: text/css\r\n"
    elif filetype == 'jpg':
        # TO DO: generate proper jpg header
        http_header = "HTTP/1.0 200 OK\r\n" + "Content-Type: image/jpeg\r\n"
    elif filetype == 'js':
        http_header = "HTTP/1.0 200 OK\r\n" + "Content-Type: text/javascript; charset=UTF-8\r\n"
    elif filetype == 'ico':
        http_header = "HTTP/1.0 200 OK\r\n" + "Content-Type: image/x-icon\r\n"
    else:
        http_header = "HTTP/1.0 500 Internal Server Error\r\n\r\n"
        client_socket.send(http_header.encode())
        return
    # TO DO: read the data from the file

    data = get_file_data(url)

    if data == "NOT FOUND":
        http_response = "HTTP/1.0 404 Not Found\r\n\r\n".encode()
    if data == "FORBIDDEN":
        http_response = "HTTP/1.0 403 Forbidden\r\n\r\n".encode()
    else:
        http_response = http_header.encode() + data

    client_socket.send(http_response)


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    # TO DO: write function
    html_request = request.split("\r\n")
    html_request = html_request[0].split(" ")
    if len(html_request) == 3:
        if html_request[0] == "GET" and html_request[2] == "HTTP/1.1":
            return True, html_request[1]
        else:
            return False, ""
    else:
        return False, ""


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        # TO DO: insert code that receives client request
        client_request = client_socket.recv(1024).decode()
        # ...
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
