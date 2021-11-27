#   Ex. 2.7 template - client side

import socket
import protocol

IP = "127.0.0.1"
# The path + filename where the copy of the screenshot at the client should be saved
SAVED_PHOTO_LOCATION = "C:\Saved_photo\screen_transfer.jpg"


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    data = cmd.split()
    valid, server_response = protocol.get_msg(my_socket)
    if valid:
        # (8) treat all responses except SEND_PHOTO
        if data[0] == "DIR" or data[0] == "DELETE" or data[0] == "EXECUTE" or data[0] == "COPY" \
                or data[0] == "TAKE_SCREENSHOT":
            print(server_response)
        # (10) treat SEND_PHOTO
        if data[0] == "SEND_PHOTO":
            if server_response.isdigit():
                photo_size = int(server_response)
                photo = my_socket.recv(photo_size)
                write_file = open(SAVED_PHOTO_LOCATION, 'wb')
                write_file.write(photo)
                write_file.close()
                print("The image was send successfully")
            else:
                print(server_response)


def main():
    # open socket with the server
    # (2)
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()
