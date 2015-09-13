#import sys, os, time, socket, getpass, argparse
import os, socket, time, pickle

from helper import getSocketName, readQueue, writeQueue

def daemonMain():
    # Creating Socket
    socketPath= getSocketName()
    if os.path.exists(socketPath):
        os.remove(socketPath)
    try:
        daemon = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        daemon.bind(socketPath)
        daemon.setblocking(0)
    except:
        print("Daemon couldn't bind to socket. Aborting")
        sys.exit(1)
    else:
        print("Daemon got socket")

    while True:
        try:
            data = daemon.recv(1024)
        except BlockingIOError:
            data = False

        if data:
            command = pickle.loads(data)
            if command['mode'] == 'add':
                queue = readQueue()
                if len(queue) != 0:
                    nextKey = max(queue.keys()) + 1
                else:
                    nextKey = 0
                queue[nextKey] = command
                writeQueue(queue)
            elif command['mode'] == 'EXIT':
                print('Shutting down pueue daemon')
                break

        time.sleep(0.5)

    os.remove(socketPath)

