import threading
import time

import pyautogui
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLineEdit, QLabel, QHBoxLayout

from LeagueOfLegendsClientWindow import LeagueOfLegendsClientWindow

searching = False


def wait_thread(check_queue: bool):
    global searching

    if searching:
        return

    searching = True

    # TODO hide (minimize) window while search

    # TODO display current search status (only wait or search blind game)
    chat_message_box.setReadOnly(True)
    chat_message_box.setStyleSheet("background-color: lightgray;")
    champion_pick_box.setReadOnly(True)
    champion_pick_box.setStyleSheet("background-color: lightgray;")

    search_game_button.setDisabled(True)
    wait_for_game_button.setDisabled(True)

    cancel_search_button.setText("Cancel")
    cancel_search_button.setDisabled(False)

    text_to_send = chat_message_box.text()
    accepted = False
    while not accepted and searching:
        state = lol_client.get_state()
        if state == "found_game":

            lol_client.accept_game()
            accepted = True
            searching = False
            already_wrote = False
            for i in range(42):
                lol_client.send_message(text_to_send)
                time.sleep(0.03)
                # TODO update already_wrote in extra thread
                if already_wrote:
                    break

            # TODO check here for errors (only in wait for game mode? only if text marked?)
            # The error only triggers in some cases, maybe if a game was not accepted by one player and then re-found
            # TODO reimplemented reaccept logic
            # only restart after everything is done should fex
            if lol_client.in_champion_selection():
                champion_to_pick = champion_pick_box.text()
                if champion_to_pick != "":
                    lol_client.search_champion(champion_to_pick)
                    time.sleep(1)
                    lol_client.pick_first_champion()
            else:
                if lol_client.get_state() == "found_game":
                    time.sleep(2)
                accepted = False
                searching = True
        elif check_queue and state != "in_queue":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setWindowIcon(QtGui.QIcon("icon.ico"))
            msg.setWindowTitle("AutoLoLClient")
            msg.setText("Not in queue anymore, please press a start button again")

            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec()

            chat_message_box.setReadOnly(False)
            chat_message_box.setStyleSheet("background-color: white;")
            champion_pick_box.setReadOnly(False)
            champion_pick_box.setStyleSheet("background-color: white;")

            chat_message_box.setReadOnly(False)
            chat_message_box.setStyleSheet("background-color: white;")
            champion_pick_box.setReadOnly(False)
            champion_pick_box.setStyleSheet("background-color: white;")

            search_game_button.setDisabled(False)
            wait_for_game_button.setDisabled(False)

            searching = False
            return

    chat_message_box.setReadOnly(False)
    chat_message_box.setStyleSheet("background-color: white;")
    champion_pick_box.setReadOnly(False)
    champion_pick_box.setStyleSheet("background-color: white;")

    search_game_button.setDisabled(False)
    wait_for_game_button.setDisabled(False)

    cancel_search_button.setText("Waiting...")
    cancel_search_button.setDisabled(True)


def cancel():
    global searching
    searching = False


def search_game():
    user_input = pyautogui.confirm(text='Start searching for game?', title='AutoLoLClient', buttons=["OK", "Cancel"])
    if user_input == "Cancel":
        return

    if not lol_client.in_menu():
        if not lol_client.go_to_menu():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setWindowIcon(QtGui.QIcon("icon.ico"))
            msg.setWindowTitle("AutoLoLClient")
            msg.setText("Error occurred, press show details to show possible solutions")
            msg.setDetailedText("Start the lol client and login\n"
                                "Set the lol client language to english\n"
                                "Set the lol client window size to 1024x576\n"
                                "Place the lol client window in foreground of your main monitor")

            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec()

            return

    lol_client.search_game()
    search_game_waiting_thread = threading.Thread(target=wait_thread, args=(True,))
    search_game_waiting_thread.start()


def wait_for_game():
    user_input = pyautogui.confirm(text='Start waiting for game?', title='AutoLoLClient', buttons=["OK", "Cancel"])
    if user_input == "Cancel":
        return

    wait_for_game_waiting_thread = threading.Thread(target=wait_thread, args=(False,))
    wait_for_game_waiting_thread.start()


if __name__ == '__main__':
    pyautogui.alert(text='Welcome to AutoLoLClient!\n'
                         '\n'
                         'Hints:\n'
                         '# Make sure lol language is english\n'
                         '# And lol client window size is 1024x576', title='AutoLoLClient', button='OK')

    lol_client = LeagueOfLegendsClientWindow()

    app = QApplication([])
    window = QWidget()
    window.setWindowIcon(QtGui.QIcon("icon.ico"))
    window.setWindowTitle("AutoLoLClient")
    window.setMinimumWidth(400)
    window.setMinimumWidth(300)

    layout = QVBoxLayout()

    layout.addWidget(QLabel("<b>Enter message to write instantly</b><br>[leave blank for no message]"))
    chat_message_box = QLineEdit()
    chat_message_box.setPlaceholderText("mid")
    layout.addWidget(chat_message_box)

    layout.addWidget(QLabel("<b>Enter champion to pick</b> (full name)<br>[leave blank for no pick]"))
    champion_pick_box = QLineEdit()
    champion_pick_box.setPlaceholderText("Anni")
    layout.addWidget(champion_pick_box)

    layout.addWidget(QLabel("<hr>"))

    inner_layout = QHBoxLayout()

    search_game_button = QPushButton("Search Blind Pick Game")
    inner_layout.addWidget(search_game_button)
    search_game_button.clicked.connect(search_game)

    wait_for_game_button = QPushButton("Only wait for accept")
    inner_layout.addWidget(wait_for_game_button)
    wait_for_game_button.clicked.connect(wait_for_game)

    layout.addLayout(inner_layout)

    cancel_search_button = QPushButton("Waiting...")  # text will changed in other function
    cancel_search_button.setDisabled(True)
    layout.addWidget(cancel_search_button)
    cancel_search_button.clicked.connect(cancel)

    window.setLayout(layout)
    window.show()
    app.exec()
