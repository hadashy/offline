import os
import random
import shutil
import sys
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.image as mping
from games.war_game.player import Player


class WarGame:
    def __init__(self, players: list[Player], packets_paths: list[str]):
        self._players = players
        self.packets_paths = packets_paths

    @property
    def players(self) -> list[Player]:
        return self._players

    @players.setter
    def players(self, value) -> None:
        self._players = value

    @property
    def packets_paths(self) -> list[Player]:
        return self._packets_paths

    @packets_paths.setter
    def packets_paths(self, value) -> None:
        self._packets_paths = value

    def initialize_packs(self) -> None:
        for i in range(len(self._players)):
            shutil.copytree(self._packets_paths[i], self._players[i].path)

    def update_packs(
            self,
            winner: str,
            chosen_card: str,
            tie_cards_0: list[str] = None,
            tie_cards_1: list[str] = None
    ) -> None:
        if self.players[1].player == winner:
            if tie_cards_0:
                for card in tie_cards_0:
                    self.reorganize_cards(f"{self.players[0].path}{card}",
                                          f"{self.players[1].path}{card}")
            else:
                self.reorganize_cards(f"{self.players[0].path}{chosen_card}",
                                      f"{self.players[1].path}{chosen_card}")
        else:
            if tie_cards_1:
                for card in tie_cards_1:
                    self.reorganize_cards(f"{self.players[1].path}{card}",
                                          f"{self.players[0].path}{card}")
            else:
                self.reorganize_cards(f"{self.players[1].path}{chosen_card}",
                                      f"{self.players[0].path}{chosen_card}")

        for player in self.players:
            player.reorganize_pack()

    def play_round(
            self,
            rounds_counter: int,
            cards_window_size: tuple[int, int, int, int],
            cards_window_interval: int
    ) -> None:
        self.players[0].chosen_card = random.choice(self.players[0].cards)
        self.players[1].chosen_card = random.choice(self.players[1].cards)

        self.create_img_figure(rounds_counter, cards_window_size, cards_window_interval)
        self.check_round_results(rounds_counter, cards_window_size, cards_window_interval)

    def tie_round(
            self,
            rounds_counter: int,
            cards_window_size: tuple[int, int, int, int],
            cards_window_interval: int,
            tie_cards_0: list[str] = None,
            tie_cards_1: list[str] = None
    ) -> None:
        if not tie_cards_0:
            tie_cards_0 = []
            tie_cards_1 = []
        for i in range(3):
            if i <= len(self.players[0].cards):
                tie_cards_0 = self.players[0].get_random_card(tie_cards_0)
            if i <= len(self.players[1].cards):
                tie_cards_1 = self.players[1].get_random_card(tie_cards_1)

            self.create_img_figure(rounds_counter, cards_window_size, cards_window_interval)
        self.check_round_results(rounds_counter, cards_window_size, cards_window_interval, tie_cards_0, tie_cards_1)

    def check_round_results(
            self,
            rounds_counter: int,
            cards_window_size: tuple[int, int, int, int],
            cards_window_interval: int,
            tie_cards_0: list[str] = None,
            tie_cards_1: list[str] = None
    ) -> None:
        if int(self.players[0].chosen_card[:-5]) > int(self.players[1].chosen_card[:-5]):
            self.create_img_figure(rounds_counter, cards_window_size, cards_window_interval,
                                   True, self.players[0].player)
            self.update_packs(self.players[0].player, self.players[1].chosen_card,
                              tie_cards_0, tie_cards_1)
        elif int(self.players[0].chosen_card[:-5]) < int(self.players[1].chosen_card[:-5]):
            self.create_img_figure(rounds_counter, cards_window_size, cards_window_interval,
                                   True, self.players[1].player)
            self.update_packs(self.players[1].player, self.players[0].chosen_card,
                              tie_cards_0, tie_cards_1)
        else:
            if tie_cards_0:
                self.tie_round(rounds_counter, cards_window_size, cards_window_interval, tie_cards_0, tie_cards_1)
            else:
                self.tie_round(rounds_counter, cards_window_size, cards_window_interval)

    def end_game(self) -> None:
        [shutil.rmtree(player.path) for player in self._players]

    def display_game_results(self, label: tk.Label) -> None:
        if len(self.players[0].cards) > len(self.players[1].cards):
            label.config(text=f'{self.players[0].player} player has won')
        elif len(self.players[0].cards) < len(self.players[1].cards):
            label.config(text=f'{self.players[1].player} player has won')
        else:
            label.config(text='Tie')

    def create_main_window(
            self,
            rounds_counter: int,
            main_window_size: str,
            cards_window_size: tuple[int, int, int, int],
            cards_window_interval: int
    ) -> None:
        window = tk.Tk()
        window.title('War Game')
        window.geometry(main_window_size)
        window.configure(background='white')

        label = tk.Label(window, text='', font=("Helvetica", 10), background='white', padx=5, pady=5)

        next_button = tk.Button(master=window, height=2, width=10, text="Next Round", font=("Helvetica", 10),
                                command=lambda: [self.play_round(
                                    rounds_counter, cards_window_size, cards_window_interval
                                )])
        next_button.pack(padx=5, pady=5)
        end_button = tk.Button(master=window, height=2, width=10, text="End Game", font=("Helvetica", 10),
                               command=lambda: [self.display_game_results(label), label.pack(pady=20), self.end_game(),
                                                messagebox.showinfo('Info', 'War game is over'),
                                                sys.exit()])
        end_button.pack(padx=5, pady=5)
        window.mainloop()

    def create_img_figure(
            self,
            rounds_counter: int,
            cards_window_size: tuple[int, int, int, int],
            cards_window_interval: int,
            border: bool = False,
            player: str = None
    ) -> None:
        rows = 1
        columns = 2
        fig = plt.figure(figsize=(10, 7), dpi=45.0)
        fig.suptitle(f'WarGame - Round {rounds_counter}', fontsize=14)
        timer = fig.canvas.new_timer(interval=cards_window_interval)
        timer.add_callback(plt.close)
        plt.rcParams["axes.linewidth"] = 0.0

        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(cards_window_size[0], cards_window_size[1], cards_window_size[2], cards_window_size[3])

        if (border is True) and (player == self.players[0].player):
            self.create_img_border()
        fig.add_subplot(rows, columns, 1)
        plt.imshow(mping.imread(self.players[0].path + self.players[0].chosen_card))
        plt.title(self.players[0].player + ' player')
        if (border is True) and (player == self.players[1].player):
            self.create_img_border()
        else:
            plt.rcParams["axes.linewidth"] = 0.0
        fig.add_subplot(rows, columns, 2)
        plt.imshow(mping.imread(self.players[1].path + self.players[1].chosen_card))
        plt.title(self.players[1].player + ' player')

        timer.start()
        plt.show()

    @staticmethod
    def reorganize_cards(old_path: str, new_path: str) -> None:
        shutil.copyfile(old_path, new_path)
        os.remove(old_path)

    @staticmethod
    def create_img_border() -> None:
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams["axes.edgecolor"] = "yellow"
        plt.rcParams["axes.linewidth"] = 10.0
