from requests import RequestException
from orange.utils import dashboard, clear


def main():
    clear()
    try:
        dashboard()
    except KeyboardInterrupt:
        print("👋 Goodbye")
    except RequestException:
        print("❌ I can't reach the modem")
    except:
        print("❌ an error occurred")

def main():
    dashboard()
if __name__ == "__main__":
     main()
    