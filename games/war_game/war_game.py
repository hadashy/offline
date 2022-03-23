import logging
from games.war_game.player import Player
from games.war_game.war import WarGame


logger = logging.getLogger(__name__)


war_paths = dict(
    demo_red_path='./demo_cards/red/',
    demo_black_path='./demo_cards/black/',
    red_path='./cards/red/',
    black_path='./cards/black/'
)

war_gui_data = dict(
    main_window_size='400x400+8+8',
    cards_window_size=(17, 40, 400, 400),
    cards_window_interval=4000
)


def initialize_game() -> WarGame:
    logger.info("Initializing the game - cards & players settings")
    game = WarGame([Player('red', war_paths['demo_red_path']),
                    Player('black', war_paths['demo_black_path'])],
                   [war_paths['black_path'], war_paths['red_path']]
                   )
    game.initialize_packs()

    for player in game.players:
        player.reorganize_pack()

    return game


def war(game: WarGame) -> None:
    rounds_counter = 1
    game.play_round(rounds_counter, war_gui_data['cards_window_size'], war_gui_data['cards_window_interval'])
    rounds_counter += 1
    while game.players[0].cards or game.players[1].cards:
        game.create_main_window(
            rounds_counter,
            war_gui_data['main_window_size'],
            war_gui_data['cards_window_size'],
            war_gui_data['cards_window_interval']
        )


def main():
    game = initialize_game()
    war(game)


if __name__ == '__main__':
    main()
