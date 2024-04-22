from loguru import logger

from topdown import Topdown, Physics

if __name__ == "__main__":
    topdown = Topdown()
    topdown.loop()