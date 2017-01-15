import os
import sys
import stat
import socket
import pickle



def receive_data(socket):
    """Receive an answer from the daemon and return the response.

    Args:
    socket (socket.socket): A socket that is connected to the daemon.

    Returns:
        dir or string: The unpickled answer.
    """
    answer = socket.recv(1048576)
    response = pickle.loads(answer)
    socket.close()
    return response


def process_response(response):
    """Print a response message and exit with 1, if the response wasn't an success."""
    # Print it and exit with 1 if operation wasn't successful
    print(response['message'])
    if response['status'] != 'success':
        sys.exit(1)


def connect_client_socket(root_dir):
    """Connect to a daemon's socket.

    Args:
        root_dir (str): The directory that used as root by the daemon.

    Returns:
        socket.socket: A socket that is connected to the daemon.
    """
    # Get config directory where the daemon socket is located
    config_dir = os.path.join(root_dir, '.config/pueue')

    # Create Socket and exit with 1, if socket can't be created
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        socket_path = os.path.join(config_dir, 'pueue.sock')
        client.connect(socket_path)
    except:
        print("Error connecting to socket. Make sure the daemon is running")
        sys.exit(1)
    return client


def create_daemon_socket(config_dir):
    """Create a socket for the daemon, depending on the directory location."""

    socket_path = os.path.join(config_dir, 'pueue.sock')
    # Create Socket and exit with 1, if socket can't be created
    try:
        daemon = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        daemon.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        daemon.bind(socket_path)
        daemon.setblocking(0)
        daemon.listen(0)
        # Set file permissions
        os.chmod(socket_path, stat.S_IRWXU)
    except:
        print("Daemon couldn't bind to socket. Aborting")
        sys.exit(1)
    return daemon
