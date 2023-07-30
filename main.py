from internal.game import Game
from pkg import get_config


#TODO: SFX, End Menu, Score System, Increasing difficulty, *Double Jump
# * - not necessary

def main():
    cfg = get_config("./config/config.json")

    game = Game(cfg)
    game.start()


if __name__ == '__main__':
    main()
