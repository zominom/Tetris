from constants import WIDTH, HEIGHT, DEVICE_MAC, CHAR_UUID
from board import Board
from Shapes import IShape, SShape, OShape, TShape, ZShape, JShape, LShape

from random import choice
from pynput.keyboard import Key, Listener
from bleak import BleakClient
import asyncio

from utils import send_frame, activate_fun_mode
from constants import NUMBER_OF_PLAYERS

class Game():
    def __init__(self, width=WIDTH, height=HEIGHT):
        self._width = width
        self._height = height
        self._board_width = width // NUMBER_OF_PLAYERS - 2
        self._boards: list[Board] = [Board(self._board_width, height) for _ in range(NUMBER_OF_PLAYERS)]
        self._current_pieces = [None] * NUMBER_OF_PLAYERS
        self._current_positions = [None] * NUMBER_OF_PLAYERS
        self._spawning_position = (self._board_width // 2, 0)
        self._game_over = [False] * NUMBER_OF_PLAYERS
        self._scores = [0] * NUMBER_OF_PLAYERS

        self._current_turn = 0

    def spawn_pieces(self):
        self._current_pieces = [
            choice(
                [IShape.IShape, SShape.SShape, OShape.OShape, TShape.TShape, ZShape.ZShape, JShape.JShape, LShape.LShape]
                )() for _ in range(NUMBER_OF_PLAYERS)
        ]
        self._current_positions = [self._spawning_position] * NUMBER_OF_PLAYERS

        return [
            self._boards[i].draw_shape(self._current_pieces[i], self._spawning_position) for i in range(NUMBER_OF_PLAYERS)
        ]
    
    def spawn_piece(self, player_index):
        self._current_pieces[player_index] = choice(
            [IShape.IShape, SShape.SShape, OShape.OShape, TShape.TShape, ZShape.ZShape, JShape.JShape, LShape.LShape]
            )()
        self._current_positions[player_index] = self._spawning_position

        return self._boards[player_index].draw_shape(self._current_pieces[player_index], self._spawning_position)
    
    def next_turn(self):
        for _ in range(NUMBER_OF_PLAYERS):
            self._current_turn = (self._current_turn + 1) % NUMBER_OF_PLAYERS
            if not self._game_over[self._current_turn]:
                break

    def is_game_over(self, player_index):
        return not self._boards[player_index].is_drawable(self._current_pieces[player_index], self._spawning_position)

    def on_press(self, key):
        player_index = self._current_turn
        if player_index >= NUMBER_OF_PLAYERS or self._game_over[player_index]:
            return

        if key == Key.left:
            self._current_positions[player_index] = self._boards[player_index].move_shape_left(self._current_pieces[player_index], self._current_positions[player_index])
        elif key == Key.right:
            self._current_positions[player_index] = self._boards[player_index].move_shape_right(self._current_pieces[player_index], self._current_positions[player_index])
        elif key == Key.up:
            self._boards[player_index].rotate_shape(self._current_pieces[player_index], self._current_positions[player_index])
        elif key == Key.down:
            self._current_positions[player_index] = self._boards[player_index].move_shape_down(self._current_pieces[player_index], self._current_positions[player_index])
            self._current_positions[player_index] = self._boards[player_index].move_shape_down(self._current_pieces[player_index], self._current_positions[player_index])

    async def _run_game(self, client, player_index):
        while not self._game_over[player_index]:
            if player_index != self._current_turn:
                await asyncio.sleep(0.05)
                continue

            last_position = self._current_positions[player_index]

            await send_frame(client, self._boards, self._scores)

            print(f"Player {player_index} piece position: {self._current_positions[player_index]}")
            self._current_positions[player_index] = self._boards[player_index].move_shape_down(self._current_pieces[player_index], self._current_positions[player_index])
            self._scores[player_index] += self._boards[player_index].clear_lines() * 100

            if self._current_positions[player_index] == last_position:
                if self.is_game_over(player_index):
                        self._game_over[player_index] = True
                        print(f"Game over for player {player_index}")
                        print(f"Player {player_index} score: {self._scores[player_index]}")

                        self.next_turn()
                        await asyncio.sleep(0.5)
                        break
                
                self.spawn_piece(player_index)
                self._scores[player_index] += 20

                self.next_turn()
                await asyncio.sleep(0.5)

            await asyncio.sleep(0.1)

    async def run(self):
        self.spawn_pieces()

        listener = Listener(on_press=self.on_press)
        listener.start()

        async with BleakClient(DEVICE_MAC) as client:
            await client.write_gatt_char(CHAR_UUID, activate_fun_mode())
            await asyncio.sleep(0.5)

            game_tasks = [asyncio.create_task(self._run_game(client, i)) for i in range(NUMBER_OF_PLAYERS)]

            await asyncio.gather(*game_tasks)

        listener.join()