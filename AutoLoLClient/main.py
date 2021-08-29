import time

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from AutoLoLClient.LeagueOfLegendsClientWindow import LeagueOfLegendsClientWindow

if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("AutoLoLClient")
    window.setMinimumWidth(400)
    window.setMinimumWidth(300)

    layout = QVBoxLayout()

    window.setLayout(layout)
    window.show()
    app.exec()

    lol_client = LeagueOfLegendsClientWindow()
    accepted = False
    while not accepted:
        state = lol_client.get_state()
        if state == "found_game":

            lol_client.accept_game()
            accepted = True
            for i in range(30):
                lol_client.send_message("mid")
                time.sleep(0.03)
