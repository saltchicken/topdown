from loguru import logger

from engine import Topdown

if __name__ == "__main__":
    topdown = Topdown()
    topdown.loop()