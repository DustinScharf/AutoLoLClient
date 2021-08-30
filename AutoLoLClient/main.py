import time

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLineEdit, QLabel, QHBoxLayout

from LeagueOfLegendsClientWindow import LeagueOfLegendsClientWindow


def search_game():
    if not lol_client.in_menu():
        if not lol_client.go_to_menu():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setWindowTitle("AutoLoLClient")
            msg.setText("Error occurred, press show details to show possible solutions")
            msg.setDetailedText("Put the lol client window into the foreground\n"
                                "Put the lol client window to you main monitor\n"
                                "Set the lol client language to english\n"
                                "Set the lol client window size to 1024x576")

            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec()

            return

    lol_client.search_game()
    text_to_send = chat_message_box.text()
    accepted = False
    while not accepted:
        state = lol_client.get_state()
        if state == "found_game":

            lol_client.accept_game()
            accepted = True
            for i in range(30):
                lol_client.send_message(text_to_send)
                time.sleep(0.03)

            if lol_client.in_champion_selection():
                lol_client.search_champion(champion_pick_box.text())
                time.sleep(1)
                lol_client.pick_first_champion()
            else:
                accepted = False
        elif state != "in_queue":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setWindowTitle("AutoLoLClient")
            msg.setText("Not in queue anymore, please press a start button again")

            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec()

            return


def wait_for_game():
    text_to_send = chat_message_box.text()
    accepted = False
    while not accepted:
        state = lol_client.get_state()
        if state == "found_game":

            lol_client.accept_game()
            accepted = True
            for i in range(30):
                lol_client.send_message(text_to_send)
                time.sleep(0.03)

            if lol_client.in_champion_selection():
                lol_client.search_champion(champion_pick_box.text())
                time.sleep(1)
                lol_client.pick_first_champion()
            else:
                accepted = False
        elif state != "in_queue":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setWindowTitle("AutoLoLClient")
            msg.setText("Not in queue anymore, please press a start button again")

            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec()

            return


if __name__ == '__main__':
    lol_client = LeagueOfLegendsClientWindow()

    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("AutoLoLClient")
    window.setMinimumWidth(400)
    window.setMinimumWidth(300)

    layout = QVBoxLayout()

    layout.addWidget(QLabel("Enter message to write instantly"))
    chat_message_box = QLineEdit()
    layout.addWidget(chat_message_box)

    layout.addWidget(QLabel("Enter champion to pick (full name)"))
    champion_pick_box = QLineEdit()
    layout.addWidget(champion_pick_box)

    inner_layout = QHBoxLayout()

    search_game_button = QPushButton("Search Blind Pick Game")
    inner_layout.addWidget(search_game_button)
    search_game_button.clicked.connect(search_game)

    wait_for_game_button = QPushButton("Only wait for accept")
    inner_layout.addWidget(wait_for_game_button)
    search_game_button.clicked.connect(wait_for_game)

    layout.addLayout(inner_layout)

    window.setLayout(layout)
    window.show()
    app.exec()
