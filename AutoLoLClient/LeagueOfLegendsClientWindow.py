import time
from typing import Tuple

import pyautogui
import win32con
from win32api import MAKELONG, SetCursorPos, mouse_event, GetMonitorInfo, EnumDisplayMonitors
from win32con import WM_LBUTTONDOWN, MK_LBUTTON, MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP

from win32gui import FindWindow, GetWindowRect, PostMessage, SetForegroundWindow, MoveWindow, ShowWindow, \
    GetWindowPlacement, SetActiveWindow


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
        league_of_legends_window_y = league_of_legends_window_rect[1]
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
            start_game_detection_icon = pyautogui.locateCenterOnScreen('play.png', confidence=0.8)
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
            queue_detection_icon = pyautogui.locateCenterOnScreen('queue.png', confidence=0.99)
            queue_detection_icon_found = queue_detection_icon is not None
            if queue_detection_icon_found:
                found_or_not_found += 1
            else:
                found_or_not_found -= 1

        in_queue = found_or_not_found > 0
        return in_queue

    def found_game(self) -> bool:
        if not self.is_open():
            return False

        # TODO use accept button, because of different game modes
        game_found_detection_icon = pyautogui.locateCenterOnScreen('found.png', confidence=0.9)
        game_found = game_found_detection_icon is not None
        return game_found

    def go_to_menu(self) -> bool:
        if not self.is_open():
            return False

        if not self.get_size() == [1024, 576]:
            return False

        if self.in_menu():
            return True

        # TODO experimental, can cause bugs
        # self.force_foreground()

        party_detection_icon = pyautogui.locateCenterOnScreen('party.png', confidence=0.8)
        party_detection_icon_found = party_detection_icon is not None
        if party_detection_icon_found:
            pyautogui.click(party_detection_icon.x, party_detection_icon.y)
            time.sleep(2)

            leave_lobby_detection_icon = pyautogui.locateCenterOnScreen('leave_lobby.png', confidence=0.9)
            pyautogui.click(leave_lobby_detection_icon.x, leave_lobby_detection_icon.y)
            time.sleep(2)
            return True

        menu_detection_icon_0 = pyautogui.locateCenterOnScreen('home_button.png', confidence=0.8)
        menu_detection_icon_0_found = menu_detection_icon_0 is not None
        if menu_detection_icon_0_found:
            pyautogui.click(menu_detection_icon_0.x, menu_detection_icon_0.y)
            time.sleep(2)
            return True

        menu_detection_icon_1 = pyautogui.locateCenterOnScreen('menu_after_game.png', confidence=0.999)
        menu_detection_icon_1_found = menu_detection_icon_1 is not None
        if menu_detection_icon_1_found:
            pyautogui.click(menu_detection_icon_1.x, menu_detection_icon_1.y)
            time.sleep(2)

            leave_party_detection_icon_1 = pyautogui.locateCenterOnScreen('leave_party.png', confidence=0.9)
            leave_party_detection_icon_1_found = leave_party_detection_icon_1 is not None
            if leave_party_detection_icon_1_found:
                pyautogui.click(leave_party_detection_icon_1.x, leave_party_detection_icon_1.y)
                time.sleep(2)

            leave_party_detection_icon_2 = pyautogui.locateCenterOnScreen('leave_party_2.png', confidence=0.9)
            leave_party_detection_icon_2_found = leave_party_detection_icon_2 is not None
            if leave_party_detection_icon_2_found:
                pyautogui.click(leave_party_detection_icon_2.x, leave_party_detection_icon_2.y)
                time.sleep(2)

            return True

        return False

    def search_game(self) -> bool:
        if not self.is_open():
            return False

        # TODO LANGUAGE SPECIFIC
        start_game_detection_icon = pyautogui.locateCenterOnScreen('play.png', confidence=0.8)
        start_game_detection_icon_found = start_game_detection_icon is not None
        if start_game_detection_icon_found:
            pyautogui.click(start_game_detection_icon.x, start_game_detection_icon.y)
            time.sleep(2)

        summoners_rift_detection_icon = pyautogui.locateCenterOnScreen('5v5sumRift.png', confidence=0.999)
        summoners_rift_detection_icon_found = summoners_rift_detection_icon is not None
        if summoners_rift_detection_icon_found:
            pyautogui.click(summoners_rift_detection_icon.x, summoners_rift_detection_icon.y)
            time.sleep(2)

        blind_pick_detection_icon = pyautogui.locateCenterOnScreen('blind_pick.png', confidence=0.9)
        blind_pick_detection_icon_found = blind_pick_detection_icon is not None
        if blind_pick_detection_icon_found:
            pyautogui.click(blind_pick_detection_icon.x, blind_pick_detection_icon.y)
            time.sleep(2)

        confirm_detection_icon = pyautogui.locateCenterOnScreen('confirm.png', confidence=0.999)
        confirm_detection_icon_found = confirm_detection_icon is not None
        if confirm_detection_icon_found:
            pyautogui.click(confirm_detection_icon.x, confirm_detection_icon.y)
            time.sleep(3)

        find_detection_icon = pyautogui.locateCenterOnScreen('find.png', confidence=0.8)
        find_detection_icon_found = find_detection_icon is not None
        if not find_detection_icon_found:
            return False

        pyautogui.click(find_detection_icon.x, find_detection_icon.y)
        time.sleep(2)

        success = self.in_queue() or self.found_game()
        return success

    def accept_game(self) -> bool:
        if not self.is_open():
            return False

        # TODO LANGUAGE SPECIFIC
        accept_game_detection_icon = pyautogui.locateCenterOnScreen('accept.png', confidence=0.8)
        pyautogui.click(accept_game_detection_icon.x, accept_game_detection_icon.y)
        return True

    def send_message(self, message: str):
        window_pos = self.get_pos()
        window_size = self.get_size()
        x = window_pos[0] + 100
        y = window_pos[1] + window_size[1] - 30
        SetCursorPos((x, y))
        mouse_event(MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        mouse_event(MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        pyautogui.write(message)
        pyautogui.press("enter")

    def in_champion_selection(self) -> bool:
        if not self.is_open():
            return False

        # TODO LANGUAGE SPECIFIC
        search_detection_icon = pyautogui.locateCenterOnScreen('search_champion.png', confidence=0.85)
        search_detection_icon_found = search_detection_icon is not None
        return search_detection_icon_found

    def search_champion(self, champion_name: str) -> bool:
        if not self.in_champion_selection():
            return False

        search_detection_icon = pyautogui.locateCenterOnScreen('search_champion.png', confidence=0.9)
        pyautogui.click(search_detection_icon.x, search_detection_icon.y)
        pyautogui.write(champion_name, interval=0.05)
        time.sleep(0.2)
        return True

    def pick_first_champion(self) -> bool:
        window_pos = self.get_pos()
        x = window_pos[0] + 300
        y = window_pos[1] + 125
        SetCursorPos((x, y))
        time.sleep(0.2)
        mouse_event(MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        mouse_event(MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(0.2)

        lock_in_detection_icon = pyautogui.locateCenterOnScreen('lock_champion.png', confidence=0.9)
        lock_in_detection_icon_found = lock_in_detection_icon is not None
        if not lock_in_detection_icon_found:
            return False

        pyautogui.click(lock_in_detection_icon.x, lock_in_detection_icon.y)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
        return True

    def get_state(self) -> str:
        if self.found_game():
            return "found_game"
        elif self.in_queue():
            return "in_queue"
        elif self.in_menu():
            return "in_menu"
        else:
            return "other"

    def force_foreground(self):
        if not self.is_open():
            return False

        main_monitor = None
        for monitor_full_info in EnumDisplayMonitors():
            monitor_py_handle = str(monitor_full_info[0])[:-1].partition("PyHANDLE:")[2]
            monitor_flag = GetMonitorInfo(int(monitor_py_handle))['Flags']
            if monitor_flag == 1:
                main_monitor = monitor_full_info
                break

        if main_monitor is None:
            return False

        main_monitor_x = main_monitor[2][0]
        main_monitor_y = main_monitor[2][1]

        ShowWindow(self.league_of_legends_window, win32con.SW_SHOW)
        time.sleep(0.25)
        SetForegroundWindow(self.league_of_legends_window)
        time.sleep(0.25)
        SetActiveWindow(self.league_of_legends_window)
        time.sleep(0.25)
        MoveWindow(self.league_of_legends_window, main_monitor_x, main_monitor_y, 1024, 576, True)
        time.sleep(0.5)
