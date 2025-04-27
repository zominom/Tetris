from random import choice, randint
from threading import Thread

from pynput.keyboard import Key, Listener
from bleak import BleakClient
import asyncio

from board import Board
from Shapes import IShape, SShape, OShape, TShape, ZShape, JShape, LShape
from utils import send_frame, activate_fun_mode
from constants import DEVICE_MAC, CHAR_UUID, WIDTH, HEIGHT

class Game(Thread):
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._board = Board(width, height)
        self._current_piece = None
        self._current_postion = None
        self._game_over = False
        self._score = 0

    def spawn_piece(self):
        self._current_piece = choice([IShape.IShape, SShape.SShape, OShape.OShape, TShape.TShape, ZShape.ZShape, JShape.JShape, LShape.LShape])()
        self._current_postion = (randint(0, self._width - 1), 0)
        return self._board.draw_shape(self._current_piece, self._current_postion)

    def on_press(self, key):
        if key == Key.left:
            self._current_postion = self._board.move_shape_left(self._current_piece, self._current_postion)
        elif key == Key.right:
            self._current_postion = self._board.move_shape_right(self._current_piece, self._current_postion)
        elif key == Key.up:
            self._board.rotate_shape(self._current_piece, self._current_postion)
        elif key == Key.down:
            self._current_postion = self._board.move_shape_down(self._current_piece, self._current_postion)
            self._current_postion = self._board.move_shape_down(self._current_piece, self._current_postion)
        

    async def run(self):
        self.spawn_piece()

        async with BleakClient(DEVICE_MAC) as client, Listener(on_press=self.on_press) as listener:
            await client.write_gatt_char(CHAR_UUID, activate_fun_mode())
            await asyncio.sleep(0.5)

            while not self._game_over:
                await send_frame(client, self._board)
                last_position = self._current_postion

                self._current_postion = self._board.move_shape_down(self._current_piece, self._current_postion)
                self._score += self._board.clear_lines() * 1000

                if self._current_postion == last_position:
                    if not self.spawn_piece():
                        self._game_over = True

if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    asyncio.run(game.run())