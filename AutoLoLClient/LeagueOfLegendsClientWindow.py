import time
from typing import Tuple

import pyautogui

from win32gui import FindWindow, GetWindowRect


class LeagueOfLegendsClientWindow(object):
    def __init__(self, window_name: str = "League of Legends"):
        self.window_name = window_name

        self.league_of_legends_window = FindWindow(None, self.window_name)  # TODO exception

    def is_open(self):
        self.league_of_legends_window = FindWindow(None, self.window_name)
        window_is_open = self.league_of_legends_window != 0
        return window_is_open

    def get_pos(self) -> Tuple[int, int]:
        if not self.is_open():
            return -1, -1  # TODO exception

        league_of_legends_window_rect = GetWindowRect(self.league_of_legends_window)
        league_of_legends_window_x = league_of_legends_window_rect[0]
        league_of_legends_window_y = league_of_legends_window_rect[2]
        return league_of_legends_window_x, league_of_legends_window_y

    def get_size(self) -> Tuple[int, int]:
        if not self.is_open():
            return -1, -1  # TODO exception

        league_of_legends_window_rect = GetWindowRect(self.league_of_legends_window)

        league_of_legends_window_x = league_of_legends_window_rect[0]
        league_of_legends_window_x_end = league_of_legends_window_rect[2]

        league_of_legends_window_y = league_of_legends_window_rect[1]
        league_of_legends_window_y_end = league_of_legends_window_rect[3]

        league_of_legends_window_width = league_of_legends_window_x_end - league_of_legends_window_x
        league_of_legends_window_height = league_of_legends_window_y_end - league_of_legends_window_y

        return league_of_legends_window_width, league_of_legends_window_height

    def in_menu(self) -> bool:
        if not self.is_open():
            return False  # TODO exception

        found_or_not_found = 0
        for i in range(5):
            # TODO LANGUAGE SPECIFIC
            start_game_detection_icon = pyautogui.locateCenterOnScreen('AutoLoLClient/play.png', confidence=0.8)
            start_game_detection_icon_found = start_game_detection_icon is not None
            if start_game_detection_icon_found:
                found_or_not_found += 1
            else:
                found_or_not_found -= 1

        in_menu = found_or_not_found > 0
        return in_menu

    def in_queue(self) -> bool:
        if not self.is_open():
            return False  # TODO exception

        found_or_not_found = 0
        for i in range(5):
            queue_detection_icon = pyautogui.locateCenterOnScreen('AutoLoLClient/queue.png', confidence=0.999)
            queue_detection_icon_found = queue_detection_icon is not None
            if queue_detection_icon_found:
                found_or_not_found += 1
            else:
                found_or_not_found -= 1

        in_queue = found_or_not_found > 0
        return in_queue

    def search_game(self) -> bool:
        if not self.is_open():
            return False

        # TODO LANGUAGE SPECIFIC
        start_game_detection_icon = pyautogui.locateCenterOnScreen('AutoLoLClient/play.png', confidence=0.8)
        start_game_detection_icon_found = start_game_detection_icon is not None
        if start_game_detection_icon_found:
            pyautogui.click(start_game_detection_icon.x, start_game_detection_icon.y)
            time.sleep(1)

        summoners_rift_detection_icon = pyautogui.locateCenterOnScreen('AutoLoLClient/5v5sumRift.png', confidence=0.999)
        summoners_rift_detection_icon_found = summoners_rift_detection_icon is not None
        if summoners_rift_detection_icon_found:
            pyautogui.click(summoners_rift_detection_icon.x, summoners_rift_detection_icon.y)
            time.sleep(1)

        blind_pick_detection_icon = pyautogui.locateCenterOnScreen('AutoLoLClient/blind_pick.png', confidence=0.999)
        blind_pick_detection_icon_found = blind_pick_detection_icon is not None
        if blind_pick_detection_icon_found:
            pyautogui.click(blind_pick_detection_icon.x, blind_pick_detection_icon.y)
            time.sleep(1)

        confirm_detection_icon = pyautogui.locateCenterOnScreen('AutoLoLClient/confirm.png', confidence=0.999)
        confirm_detection_icon_found = confirm_detection_icon is not None
        if confirm_detection_icon_found:
            pyautogui.click(confirm_detection_icon.x, confirm_detection_icon.y)
            time.sleep(2)

        find_detection_icon = pyautogui.locateCenterOnScreen('AutoLoLClient/find.png', confidence=0.8)
        find_detection_icon_found = find_detection_icon is not None
        if not find_detection_icon_found:
            return False

        pyautogui.click(find_detection_icon.x, find_detection_icon.y)
        time.sleep(2)

        success = self.in_queue()
        return success
