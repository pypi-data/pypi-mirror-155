from time import sleep
from requests import post, get, Session
from bs4 import BeautifulSoup
from getpass import getpass

MIP = "192.168.0.1"

session = Session()
session.headers.update({
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
	})

def clear():
	print("\033[H\033[J", end="")

def get_pub_ip():
	return BeautifulSoup(get(f"http://{MIP}/overview.asp")
	.text, "html.parser").find("span", attrs={"class": "severFontSize fontStyle01"}).get_text()

def restart_local():
	session.post(f"http://{MIP}/goform/OrgNetworkRestart", data={"AskRgRestart": 1})
	sleep(8)
	print(
		"New public ip adress : "
		+ get_pub_ip()
	)

def restart_modem():
	session.post(f"http://{MIP}/goform/OrgRestart", data={"AskRgRestart": 0})
	clear()
	print("the modem will restart...")
	exit()

def stats_resolver(login):
	return [
		str(i).split(">")[1].split("<")[0]
		for i in BeautifulSoup(login.text, "html.parser").find_all(
			"span", {"class": "severFontSize fontStyle01"}
		)
	]

def dashboard():

	net_stats = [
		"🌐 Wifi",
		"🌍 Network access",
		"🔌 Wired network"
	]
	
	status = stats_resolver(get(f"http://{MIP}", timeout=3))

	net_stats_index = 0
	for stats in net_stats:
		print(
				stats, f": {status[net_stats_index]}",
				end=None
			)
		net_stats_index += 1

	if (
		"Incorrect password !"
		in post(
			f"http://{MIP}/goform/OrgLogin",
			data={"OrgPassword": getpass("Pass > ")},
		).text
	):
		print("❌ Incorrect password")
	else:
		print(
			"Public ip adress : "
			+ get_pub_ip()
		)
  

		choice = input(
"""Choose an option :
     1 - Change ip adress (restart local network)
     2 - Restart modem
     x - exit
> """
			)	
		match choice:
			case "1":
				restart_local()
			case "2":
				restart_modem()
			case "x":
				clear()
				exit()
			case _:
				print("❌ Invalid option")