from distutils.log import error
from requests import RequestException
from orange.utils import *


def main():
    clear()
    # try:
    dashboard()
    # except KeyboardInterrupt:
    #     print("👋 Goodbye")
    # except RequestException:
    #     print("❌ I can't reach the modem")
    # except:
    #     print("❌ an error occurred")


if __name__ == "__main__":
    main()
