#   Ex. 2.7 template - server side

import socket
import protocol
import os
import glob
import subprocess
import shutil
import pyautogui

IP = "0.0.0.0"
PHOTO_PATH = "C:\Saved_photo\screen.jpg"  # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # (6)
    # Use protocol.check_cmd first
    if protocol.check_cmd(cmd):
        data = cmd.split()
        # Then make sure the params are valid
        if data[0] == "EXIT" or data[0] == "TAKE_SCREENSHOT":
            return True, data[0], []
        if data[0] == "DIR" or data[0] == "DELETE" or data[0] == "EXECUTE":
            if os.path.exists(data[1]):
                return True, data[0], [data[1]]
            else:
                return False, data[0], [data[1]]
        if data[0] == "COPY":
            if os.path.exists(data[1]):
                return True, data[0], [data[1], data[2]]
            else:
                return False, data[0], [data[1], data[2]]
        if data[0] == "SEND_PHOTO":
            if os.path.exists(PHOTO_PATH):
                return True, data[0], []
            else:
                return False, data[0], []
    else:
        return False, "", []


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """

    # (7)
    if command == "DIR":
        directory = params[0] + "\*.*"
        files_list = glob.glob(directory)
        concatenated = " ".join(files_list)
        print(concatenated)
        return concatenated
    if command == "DELETE":
        os.remove(params[0])
        return "File deleted successfully"
    if command == "EXECUTE":
        subprocess.call(params[0])
        return "App executed successfully"
    if command == "COPY":
        create_file = open(params[1], 'w')
        create_file.close()
        shutil.copy(params[0], params[1])
        return "Copied successfully"
    if command == "TAKE_SCREENSHOT":
        image = pyautogui.screenshot()
        image.save(PHOTO_PATH)
        return "Image saved in the server"
    if command == "SEND_PHOTO":
        input_file = open(PHOTO_PATH, 'rb')
        photo = input_file.read()
        input_file.close()
        return str(len(photo))


def main():
    # open socket with client
    # (1)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:

                if command == 'EXIT':
                    break

                # (6)
                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)
                # add length field using "create_msg"
                send_response = protocol.create_msg(response)
                # send to client
                client_socket.send(send_response)

                if command == 'SEND_PHOTO':
                    # Send the data itself to the client
                    input_file = open(PHOTO_PATH, 'rb')
                    photo = input_file.read()
                    input_file.close()
                    client_socket.send(photo)
                    # (9)


            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                # send to client
                send_response = protocol.create_msg(response)
                client_socket.send(send_response)

        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            # send to client
            send_response = protocol.create_msg(response)
            client_socket.send(send_response)

            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
