import os
import random


class Player:
    def __init__(self, player: str, path: str):
        self._player = player
        self._path = path
        self._cards = []
        self._chosen_card = None

    @property
    def player(self) -> str:
        return self._player

    @player.setter
    def player(self, value) -> None:
        self._player = value

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value) -> None:
        self._path = value

    @property
    def cards(self) -> list[str]:
        return self._cards

    @cards.setter
    def cards(self, value) -> None:
        self._cards = value

    @property
    def chosen_card(self) -> str:
        return self._chosen_card

    @chosen_card.setter
    def chosen_card(self, value) -> None:
        self._chosen_card = value

    def reorganize_pack(self) -> None:
        self._cards = os.listdir(self._path)

    def get_random_card(self, tie_cards: list[str]) -> list[str]:
        while True:
            cur_card = random.choice(self.cards)
            if cur_card not in tie_cards:
                self.chosen_card = cur_card
                tie_cards.append(self.chosen_card)
                return tie_cards
