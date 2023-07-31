from internal.game import Game
from pkg import get_config


#TODO: End Menu, Improve spawn
# * - not necessary

def main():
    cfg = get_config("./config/config.json")

    game = Game(cfg)
    game.start()


if __name__ == '__main__':
    main()
