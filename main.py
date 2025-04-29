import asyncio
from board import Board
from constants import GAME_BOX_WIDTH, GAME_BOX_HEIGHT, WIDTH, HEIGHT
from utils import send_frame, activate_fun_mode
from bleak import BleakClient
from constants import DEVICE_MAC, CHAR_UUID
from random import choice, randint

from game import Game

async def main():

    game = Game(WIDTH, HEIGHT)
    await game.run()



if __name__ == "__main__":
    asyncio.run(main())