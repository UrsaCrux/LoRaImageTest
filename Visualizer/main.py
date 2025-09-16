from interpreter import Transfer
import pygame
import sys

WIDTH = 800
HEIGHT = 800
CELLSIZE = 20

#Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((255, 255, 255))
pygame.display.update()
pygame.display.set_caption("Image Visualizer")


def scale(value, src_min, src_max, dst_min, dst_max):
    """Scales a value from one range to another."""
    return int(((value - src_min) / (src_max - src_min)) * (dst_max - dst_min) + dst_min)

def rgb565_to_rgb888(color_565: bytes):
    """
    Converts a 16-bit RGB565 integer to a 24-bit RGB888 tuple (R, G, B) for Pygame.
    """
    r = int(color_565[0:5], 2)
    g = int(color_565[5:11], 2)
    b = int(color_565[11:16], 2)

    r = scale(r, 0, 31, 0, 255)
    g = scale(g, 0, 63, 0, 255)
    b = scale(b, 0, 31, 0, 255)

    return (r,g,b)
    
def get_colors(binary:bytes)->tuple[tuple[int, int, int], bool]:
    """Converts binary data to a list of RGB color tuples."""
    code = binary[0:8]
    if not code == b'10101010':
         return ((0, 0, 0), False)
    rgb565 = binary[8:24]
    colors = rgb565_to_rgb888(rgb565)
    return (colors, True)

def draw_pixel(x, y, color):
    """Draws a single pixel on the screen at (x, y) with the specified color."""
    pygame.draw.rect(screen, color, (x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE))
    pygame.display.update()

#Initialize the port and recieve continuos information
mainline = Transfer("COM3")
xpos = 0
ypos = 0

while True:
        line = mainline.getline()
        print(line)
        color, iscolor = get_colors(line)
        if iscolor:
            draw_pixel(xpos, ypos, color)
            xpos += 1
            if xpos >= WIDTH // CELLSIZE:
                xpos = 0
                ypos += 1
                if ypos >= HEIGHT // CELLSIZE:
                    ypos = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()