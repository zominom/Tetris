from bleak import BleakClient
import asyncio
from PIL import Image

from board import Board
from constants import CHAR_UUID, DEVICE_MAC, WIDTH, HEIGHT


def create_frame(board: Board):
    img = Image.new('RGB', (WIDTH, HEIGHT))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            img.putpixel((x, y), board.grid[y][x])
    return img

def get_frame_bytes(img):
    data = bytearray()
    data += b'\x09\x12\x00\x00\x00\x00\x12\x00\x00'  # header
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = img.getpixel((x, y))
            data += bytes([r, g, b])
    return data

async def send_frame(client: BleakClient, board: Board):
    img = create_frame(board)
    frame_bytes = get_frame_bytes(img)
    await client.write_gatt_char(CHAR_UUID, frame_bytes)
    await asyncio.sleep(0.1)
    

def activate_fun_mode():
    """Crafts a command to activate the drawing (fun) mode on the device."""
    return bytes.fromhex("05000401") + bytes.fromhex("01")
