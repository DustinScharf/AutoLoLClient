import time

from AutoLoLClient.LeagueOfLegendsClientWindow import LeagueOfLegendsClientWindow


if __name__ == '__main__':
    lol_client = LeagueOfLegendsClientWindow()
    while True:
        print(lol_client.in_menu())
        time.sleep(1)
