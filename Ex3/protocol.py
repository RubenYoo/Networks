"""EX 2.6 protocol implementation
"""
from datetime import date
import random

LENGTH_FIELD_SIZE = 2
PORT = 8820


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    if data == "TIME" or data == "WHORU" or data == "RAND" or data == "EXIT":
        return True
    return False


def create_msg(data):
    """Create a valid protocol message, with length field"""
    return str(len(data)).zfill(2) + data


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    size_msg = my_socket.recv(2).decode()
    if size_msg.isdigit():
        msg = my_socket.recv(int(size_msg)).decode()
        return True, msg
    else:
        return False, "Error"


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    if cmd == "WHORU":
        return "The best server in the world!"
    if cmd == "TIME":
        today = date.today()
        return today.strftime("%d/%m/%Y")
    if cmd == "RAND":
        return str(random.randint(1, 10))
    return "Server response"
