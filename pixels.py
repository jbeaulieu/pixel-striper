import sys

import click
from PIL import Image, UnidentifiedImageError

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
    resized.save("output.jpg", quality=jpeg)

    # Generate list of RGB values for the image, read pixel by pixel left to right, top to bottom. Takes the form
    # of a list of tuples, where each tuple is three ints representing the R,G,B values of a single pixel.
    pixels = list(resized.getdata())

if __name__ == '__main__':
    main()
