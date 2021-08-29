import time

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLineEdit, QLabel

from AutoLoLClient.LeagueOfLegendsClientWindow import LeagueOfLegendsClientWindow


def search_game():
    lol_client = LeagueOfLegendsClientWindow()

    if not lol_client.in_menu():
        if not lol_client.go_to_menu():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setWindowTitle("AutoLoLClient")
            msg.setText("Please go to the main menu")

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


if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("AutoLoLClient")
    window.setMinimumWidth(400)
    window.setMinimumWidth(300)

    layout = QVBoxLayout()

    layout.addWidget(QLabel("Enter message to write instantly"))

    chat_message_box = QLineEdit()
    layout.addWidget(chat_message_box)

    search_game_button = QPushButton("Search Blind Pick Game")
    layout.addWidget(search_game_button)
    search_game_button.clicked.connect(search_game)

    window.setLayout(layout)
    window.show()
    app.exec()
