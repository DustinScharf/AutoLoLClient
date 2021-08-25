from AutoLoLClient.LeagueOfLegendsClientWindow import LeagueOfLegendsClientWindow

if __name__ == '__main__':
    lol_client_window = LeagueOfLegendsClientWindow()
    print(f"Pos: {lol_client_window.get_pos()}")
    print(f"Size: {lol_client_window.get_size()}")

    print(f"In Queue: {lol_client_window.in_queue()}")
