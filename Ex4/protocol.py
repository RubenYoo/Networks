#   Ex. 2.7 template - protocol

LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    # (3)
    command = data.split()

    if len(command) == 1:
        if command[0] == "EXIT" or command[0] == "TAKE_SCREENSHOT" or command[0] == "SEND_PHOTO":
            return True
        else:
            return False

    if len(command) == 2:
        if command[0] == "DIR" or command[0] == "DELETE" or command[0] == "EXECUTE":
            return True
        else:
            return False

    if len(command) == 3:
        if command[0] == "COPY":
            return True
        else:
            return False

    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    # (4)
    return (str(len(data)).zfill(LENGTH_FIELD_SIZE) + data).encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    # (5)
    size_msg = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if size_msg.isdigit():
        msg = my_socket.recv(int(size_msg)).decode()
        return True, msg
    else:
        return False, "Error"


