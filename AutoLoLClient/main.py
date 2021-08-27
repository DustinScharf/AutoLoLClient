import threading
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QMessageBox

from AutoLoLClient.LeagueOfLegendsClientWindow import LeagueOfLegendsClientWindow


def refresh():
    in_menu = lol_client.in_menu()
    in_menu_label.setText(f"In Menu: {in_menu}")
    if in_menu:
        in_menu_label.setStyleSheet("background-color: green")
    else:
        in_menu_label.setStyleSheet("background-color: red")

    in_queue = lol_client.in_queue()
    in_queue_label.setText(f"In Queue: {in_queue}")
    if in_queue:
        in_queue_label.setStyleSheet("background-color: green")
    else:
        in_queue_label.setStyleSheet("background-color: red")

    game_found = lol_client.found_game()
    game_found_label.setText(f"Game Found: {game_found}")
    if game_found:
        game_found_label.setStyleSheet("background-color: green")
    else:
        game_found_label.setStyleSheet("background-color: red")





def search_game():
    lol_client.search_game()


if __name__ == '__main__':
    lol_client = LeagueOfLegendsClientWindow()

    app = QApplication([])
    app.setStyle('Windows')

    window = QWidget()
    window.setWindowTitle("AutoLoLClient")
    window.setMinimumWidth(400)
    window.setMinimumWidth(300)

    layout = QVBoxLayout()

    in_menu_label = QLabel(f"In Menu: {lol_client.in_menu()}")
    layout.addWidget(in_menu_label)

    in_queue_label = QLabel(f"In Queue: {lol_client.in_queue()}")
    layout.addWidget(in_queue_label)

    game_found_label = QLabel(f"Game Found: {lol_client.found_game()}")
    layout.addWidget(game_found_label)

    top_button = QPushButton("Search Blind Pick Game")
    layout.addWidget(top_button)
    top_button.clicked.connect(search_game)

    status_label = QLabel(f"Status: {'TODO'}")  # PLACEHOLDER TODO
    layout.addWidget(status_label)
    status_label.setStyleSheet("background-color: yellow")

    timer = QTimer()
    timer.timeout.connect(refresh)
    timer.start(3000)

    window.setLayout(layout)
    window.show()
    app.exec()
