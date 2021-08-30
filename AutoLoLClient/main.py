import time

import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLineEdit, QLabel, QHBoxLayout

from LeagueOfLegendsClientWindow import LeagueOfLegendsClientWindow
from win32api import GetMonitorInfo, EnumDisplayMonitors
from win32gui import MoveWindow


def search_game():
    user_input = pyautogui.confirm(text='Start searching for game?', title='AutoLoLClient', buttons=["OK", "Cancel"])
    if user_input == "Cancel":
        return

    if not lol_client.in_menu():
        if not lol_client.go_to_menu():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setWindowTitle("AutoLoLClient")
            msg.setText("Error occurred, press show details to show possible solutions")
            msg.setDetailedText("Set the lol client language to english\n"
                                "Set the lol client window size to 1024x576\n"
                                "Make sure the client window is in foreground of your main monitor")

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
                champion_to_pick = champion_pick_box.text()
                if champion_to_pick != "":
                    lol_client.search_champion(champion_to_pick)
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
    user_input = pyautogui.confirm(text='Start waiting for game?', title='AutoLoLClient', buttons=["OK", "Cancel"])
    if user_input == "Cancel":
        return

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
                champion_to_pick = champion_pick_box.text()
                if champion_to_pick != "":
                    lol_client.search_champion(champion_to_pick)
                    time.sleep(1)
                    lol_client.pick_first_champion()
            else:
                accepted = False


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

    layout.addWidget(QLabel("Enter champion to pick (full name) [leave blank for no pick]"))
    champion_pick_box = QLineEdit()
    layout.addWidget(champion_pick_box)

    inner_layout = QHBoxLayout()

    search_game_button = QPushButton("Search Blind Pick Game")
    inner_layout.addWidget(search_game_button)
    search_game_button.clicked.connect(search_game)

    wait_for_game_button = QPushButton("Only wait for accept")
    inner_layout.addWidget(wait_for_game_button)
    wait_for_game_button.clicked.connect(wait_for_game)

    layout.addLayout(inner_layout)

    window.setLayout(layout)
    window.show()
    app.exec()
