from random import choice, randint
from threading import Thread

from pynput.keyboard import Key, Listener
from bleak import BleakClient
import asyncio

from board import Board
from Shapes import IShape, SShape, OShape, TShape, ZShape, JShape, LShape
from utils import send_frame, activate_fun_mode
from utils import DEVICE_MAC, CHAR_UUID, WIDTH, HEIGHT

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
        self._current_piece = choice([IShape.IShape(), SShape.SShape(), OShape.OShape(), TShape.TShape(), ZShape.ZShape(), JShape.JShape(), LShape.LShape()])
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
        with Listener(on_press=self.on_press) as listener:
            async with BleakClient(DEVICE_MAC) as client:
                await client.write_gatt_char(CHAR_UUID, activate_fun_mode())
                await asyncio.sleep(0.5)
                # Start the Tetris game
                while True:
                    last_position = self._current_postion
                    await send_frame(client, self._board)

                    self._current_postion = self._board.move_shape_down(self._current_piece, self._current_postion)
                    self._board.clear_lines()

                    while self._current_postion == last_position:
                        self._current_postion = (randint(6, 90), 0)
                        self._current_piece = choice([IShape.IShape, SShape.SShape, OShape.OShape, TShape.TShape, ZShape.ZShape, JShape.JShape, LShape.LShape])()
                        
                        if not self.spawn_piece():
                            self._current_postion = last_position

if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    game.spawn_piece()
    asyncio.run(game.run())