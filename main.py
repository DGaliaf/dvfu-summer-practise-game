from internal import Game
from pkg import getConfig


def main():
    cfg = getConfig("./config/config.json")

    game = Game(cfg)
    game.start()


if __name__ == '__main__':
    main()
