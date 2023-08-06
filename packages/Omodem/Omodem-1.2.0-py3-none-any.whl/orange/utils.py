from time import sleep
from requests import post, get
from bs4 import BeautifulSoup
from getpass import getpass

mip = "192.168.0.1"
headers = { 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}

def clear():
    print("\033[H\033[J", end="")


def restart_local():
    post(f"http://{mip}/goform/OrgNetworkRestart", data={"AskRgRestart": 1}, headers=headers)
    sleep(10)
    print(
        "New public ip adress : "
        + BeautifulSoup(get(f"http://{mip}/overview.asp").text, "html.parser")
        .find("span", attrs={"class": "severFontSize fontStyle01"})
        .get_text()
    )

def restart_modem():
    post(f"http://{mip}/goform/OrgRestart", data={"AskRgRestart": 1}, headers=headers)
    print("Modem restarting...")
    exit()

def dashboard():
    login = get(f"http://{mip}", timeout=3)
    stats = [
        str(i).split(">")[1].split("<")[0]
        for i in BeautifulSoup(login.text, "html.parser").find_all(
            "span", {"class": "severFontSize fontStyle01"}
        )
    ]
    print(
        f"\n🌐 Wifi : {stats[0]}\n🌍 Network access : {stats[1]}\n🔌 Wired network : {stats[2]}\n"
    )

    if (
        "Incorrect password !"
        in post(
            f"http://{mip}/goform/OrgLogin",
            data={"OrgPassword": getpass("Pass > ")},
        ).text
    ):
        print("❌ Incorrect password")
    else:
        print(
            "Public ip adress : "
            + BeautifulSoup(get(f"http://{mip}/overview.asp").text, "html.parser")
            .find("span", attrs={"class": "severFontSize fontStyle01"})
            .get_text()
        )
        choice = int(
            input(
                "Choose an option : \n1️⃣ - Change ip adress (restart local network)\n2️⃣ - Restart modem\n\n> "
            )
        )
        if choice == 1:
            restart_local()
        elif choice == 2:
            restart_modem()
        else:
            exit()
