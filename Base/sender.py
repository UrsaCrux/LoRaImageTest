import PIL
import PIL.Image
from communication import Transfer, HEAD, IMAGE_TYPE, Packet

mainline = Transfer("COM3", timeout=5)

def rgb888_to_rgb565(r: int, g: int, b: int) -> bytes:
    """
    Converts 24-bit RGB888 values to a 16-bit RGB565 byte representation.

    Parameters
    ----------
    r : int
        Red component (0-255).
    g : int
        Green component (0-255).
    b : int
        Blue component (0-255).

    Returns
    -------
    bytes
        2-byte representation of the color in RGB565 format.
    """
    r_565 = (r >> 3) & 0x1F
    g_565 = (g >> 2) & 0x3F
    b_565 = (b >> 3) & 0x1F

    rgb565 = (r_565 << 11) | (g_565 << 5) | b_565
    return rgb565.to_bytes(2, byteorder='big')


# Ensure image size is a multiple of 8
SIZE = 480
if (SIZE * SIZE) % 8 != 0:
    SIZE = ((SIZE * SIZE) // 8) * 8
    SIZE = int(SIZE ** 0.5)  # Make it square again (approximate)
    SIZE = SIZE if (SIZE * SIZE) % 8 == 0 else SIZE + 1

print(SIZE*SIZE)
img = PIL.Image.open("DAMN.jpeg")
img = img.convert("RGB")
img = img.resize((SIZE, SIZE))
pixs = tuple(img.getdata())

for idx in range(0, SIZE*SIZE, 8):
    print(idx)
    group = pixs[idx:idx+8]
    colors = b''.join(rgb888_to_rgb565(r, g, b) for r, g, b in group)
    packet = Packet(HEAD, IMAGE_TYPE, timestamp=b'\x00\x00\x00\x00', data=colors, crc=b'\x00\x00', verbose=False)
    mainline.send_packet(packet)
    print(f"Sent pixels {idx} to {idx+7} as packet: {packet}")