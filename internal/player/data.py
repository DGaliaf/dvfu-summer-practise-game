from typing import Any


def get_best_score(cfg: dict[str, Any]) -> int:
    data_path = cfg.get("paths").get("data")

    with open(data_path + "/player.txt", "r") as data:
        lines = data.readlines()

        for line in lines:
            line = line.strip()

            n, v = line.split("=")

            if n == "BEST_SCORE":
                return v

    return 0


def write_best_score(cfg: dict[str, Any], score: int) -> None:
    data_path = cfg.get("paths").get("data")

    with open(data_path + "/player.txt", "w") as data:
        data.write(f"BEST_SCORE={score}")
