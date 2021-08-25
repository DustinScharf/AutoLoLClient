import threading
import time

from AutoLoLClient.LeagueOfLegendsClientWindow import LeagueOfLegendsClientWindow

import PySimpleGUI
import tkinter as tk


class StatusWindow(tk.Frame):
    def __init__(self, parent):
        super(StatusWindow, self).__init__(parent)

        self.lol_client_window = LeagueOfLegendsClientWindow()

        self.pos_label = tk.Label(self, text=f"Window Pos: {self.lol_client_window.get_pos()}")
        self.pos_label.pack(padx=20, pady=20)

        self.size_label = tk.Label(self, text=f"Window Size: {self.lol_client_window.get_size()}")
        self.size_label.pack(padx=20, pady=20)

        self.queue_label = tk.Label(self, text=f"In Queue: {self.lol_client_window.in_queue()}")
        self.queue_label.pack(padx=20, pady=20)

        update_thread = threading.Thread(target=self.update)
        update_thread.start()

    def update(self):
        while True:
            self.pos_label.config(text=f"Window Pos: {self.lol_client_window.get_pos()}")
            self.size_label.config(text=f"Window Size: {self.lol_client_window.get_size()}")
            self.queue_label.config(text=f"Window Size: {self.lol_client_window.in_queue()}")


if __name__ == '__main__':
    root = tk.Tk()
    statusWindow = StatusWindow(root)
    statusWindow.pack(fill="both", expand=True)
    root.mainloop()
