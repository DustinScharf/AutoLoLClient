import time

from AutoLoLClient.LeagueOfLegendsClientWindow import LeagueOfLegendsClientWindow

if __name__ == '__main__':
    lol_client = LeagueOfLegendsClientWindow()
    accepted = False
    while not accepted:
        state = lol_client.get_state()
        print(state)
        if state == "found_game":

            lol_client.accept_game()
            accepted = True
            for i in range(30):
                lol_client.send_message("mid")
                time.sleep(0.03)
