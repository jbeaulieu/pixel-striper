# Simple test for NeoPixels on Raspberry Pi
import sys

import click
from PIL import Image, UnidentifiedImageError

import time
import board
import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 256

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.01, auto_write=False, pixel_order=ORDER
)

SUPPORTED_FILE_TYPES = (".jpg", ".jpeg", ".png")

@click.command()
@click.option("-i", "--source", default="image.jpg", help="Name of image file to be resized. Must be placed in root directory. "+
    "If not supplied, the script will search for 'image.jpg'")
@click.option("-s", "--size", default=16, help="Width/Height to resize image to, in pixels. Defaults to 16")
@click.option("-q", "--jpeg", default=95, help="Set JPEG quality level. Defaults to 95. Warning: Setting this to 100 will disable "+
    "portions of the JPEG compression algorithm")
def main(source, size, jpeg):

    if not source.lower().endswith(SUPPORTED_FILE_TYPES):
        sys.exit("Error: File is not supported. Please use a valid .jpg, .jpeg, or .png file")

    try:
        image = Image.open(source)
    except FileNotFoundError:
        sys.exit("Error: File not found")
    except UnidentifiedImageError:
        sys.exit("Error: Image could not be opened. Check that the file is a valid .jpg, .jpeg, or .png file")

    # Convert image to RGB if it is currently in a different format (e.g. CMYK, RGBAlpha etc.)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Resize the image using nearest-neighbor interpolation
    resized = image.resize((size,size), Image.NEAREST)
    resized.save("output.png", quality=2)

    # Generate list of RGB values for the image, read pixel by pixel left to right, top to bottom. Takes the form
    # of a list of tuples, where each tuple is three ints representing the R,G,B values of a single pixel.
    pixel_list = list(resized.getdata())

    pixel_array = []

    # Place pixel RGB tuples into 2D array for easy grid reference
    # Individual tuples can be referenced as pixel_array[row][column]
    for j in range(size):
        row = []
        for i in range(size):
            row.append(pixel_list[j*size + i])
        pixel_array.append(row)

    get_image_pixels()

def get_image_pixels():
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(1)
    scaled_image = Image.open('output.png')
    image_pixels = scaled_image.load()
#     print("Image Size: ", scaled_image.size)
#     print("Image Pixel RGB: ", image_pixels[0,0])
        #image_pixels.append((r, g, b))
#     print("Image Pixels: ", image_pixels)
    for j in range(16):
        for i in range(16):
#             print("Index: ", image_pixels[j, i])
            g, r, b = image_pixels[j, i]
            if (j % 2 == 0):
                pixels[i+(j*16)] = (g, r, b)
                print(i+(j*16))
            else:
                pixels[((j+1)*16-1)-i] = (g, r, b)
                print((j*16)-i)
        pixels.show()
        time.sleep(.001)

def image_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixels[i] = image_pixels[i]
        pixels.show()
        time.sleep(wait)


    while True:
        # Comment this line out if you have RGBW/GRBW NeoPixels
        pixels.fill((255, 0, 0))
        # Uncomment this line if you have RGBW/GRBW NeoPixels
        # pixels.fill((255, 0, 0, 0))
        pixels.show()
        time.sleep(1)

        # Comment this line out if you have RGBW/GRBW NeoPixels
        pixels.fill((0, 255, 0))
        # Uncomment this line if you have RGBW/GRBW NeoPixels
        # pixels.fill((0, 255, 0, 0))
        pixels.show()
        time.sleep(1)

        # Comment this line out if you have RGBW/GRBW NeoPixels
        pixels.fill((0, 0, 255))
        # Uncomment this line if you have RGBW/GRBW NeoPixels
        # pixels.fill((0, 0, 255, 0))
        pixels.show()
        time.sleep(1)

        #rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
        get_image_pixels()
        image_cycle(0.001)  # rainbow cycle with 1ms delay per step

if __name__ == '__main__':
    main()