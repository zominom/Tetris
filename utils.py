from bleak import BleakClient
import asyncio
from PIL import Image, ImageDraw, ImageFont

from board import Board
from constants import CHAR_UUID, WIDTH, HEIGHT

def text_to_rgb_image(text: str, width, height, color=(0, 0, 0), font_size=7 , bg_color=(0, 0, 0)):
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    try:
         bbox = draw.textbbox((0, 0), text, font=font)
    except AttributeError:
         text_width, text_height = draw.textsize(text, font=font)
         bbox = (0, 0, text_width, text_height)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = (height - text_height) // 2
    y = max(0, y)

    draw.text((x, y), text, fill=color, font=font)
    return img


def create_frame(boards: list[Board], scores: list[int] = None):
    number_of_boards = len(boards)
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    
    section_width = WIDTH // number_of_boards
    border_width = 1
    score_area_width = (section_width - (border_width * 2)) // 4

    game_board_display_width = section_width - (border_width * 2) - score_area_width

    if number_of_boards == 0:
        return img

    if scores is not None and len(scores) != number_of_boards:
        raise ValueError("Length of scores list must match the number of boards.")

    for i in range(number_of_boards):
        board_start_x_on_img = i * section_width
        board_end_x_on_img = board_start_x_on_img + section_width

        border_left_x = board_start_x_on_img
        border_right_x = WIDTH - 1

        score_paste_x = board_start_x_on_img + border_width
        score_border_left_x = score_paste_x + score_area_width - 1

        for y in range(HEIGHT):
            if 0 <= border_left_x < WIDTH:
                 img.putpixel((border_left_x, y), (255, 0, 255))
            if 0 <= border_right_x < WIDTH:
                 img.putpixel((border_right_x, y), (255, 0, 255))
            if 0 <= score_border_left_x < WIDTH:
                 img.putpixel((score_border_left_x, y), (255, 0, 0))

        if scores is not None:
            score_text_img = text_to_rgb_image(
                str(scores[i]),
                width=score_area_width,
                height=HEIGHT // 2,
                color=(255, 255, 255),
                bg_color=(0, 0, 0)
            )
            if score_paste_x + score_area_width <= WIDTH:
                 img.paste(score_text_img, (score_paste_x, 0))


        board = boards[i]
        SOURCE_BOARD_WIDTH = board._width

        game_board_display_start_x = board_start_x_on_img + border_width + score_area_width
        game_board_display_end_x = board_end_x_on_img - border_width

        if game_board_display_width > 0 and game_board_display_start_x < game_board_display_end_x:
            source_x_offset_start = (SOURCE_BOARD_WIDTH - game_board_display_width) // 2

            for y in range(HEIGHT):
                source_y = y

                for x_display_in_section in range(game_board_display_width):
                    x_display_absolute = game_board_display_start_x + x_display_in_section

                    source_x = source_x_offset_start + x_display_in_section

                    if 0 <= source_x < SOURCE_BOARD_WIDTH and 0 <= y < board._height:
                         if 0 <= x_display_absolute < WIDTH and 0 <= y < HEIGHT:
                              img.putpixel((x_display_absolute, y), board.grid[source_y][source_x])
                    else:
                         if 0 <= x_display_absolute < WIDTH and 0 <= y < HEIGHT:
                              img.putpixel((x_display_absolute, y), (0, 0, 0))

    return img

def get_frame_bytes(img):
    data = bytearray()
    data += b'\x09\x12\x00\x00\x00\x00\x12\x00\x00'  # header
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = img.getpixel((x, y))
            data += bytes([r, g, b])
    return data

async def send_frame(client: BleakClient, boards: list[Board], scores: list[int] = None):
    img = create_frame(boards, scores)
    frame_bytes = get_frame_bytes(img)
    await client.write_gatt_char(CHAR_UUID, frame_bytes)
    await asyncio.sleep(0.1)
    

def activate_fun_mode():
    """Crafts a command to activate the drawing (fun) mode on the device."""
    return bytes.fromhex("05000401") + bytes.fromhex("01")
