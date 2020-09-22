# pixel-striper

Basic python script to prepare image files for display with addressable LEDs

## Prerequisites

The following python modules should be installed:

1. [Click](https://palletsprojects.com/p/click/)
  - Quick install: `~$ pip install click`
2. [Pillow](https://python-pillow.org/)
  - Quick install: `~$ pip install pillow`


## Usage

`pixels.py` will run on any valid .jpg, .jpeg, or .png file. By default, it will search for a file titled `image.jpg` in its directory, and resize that file to 16px square, output to `output.jpg`. It will also generate a two-dimensional array of RGB values for the pixels in the image, read left to right, top to bottom. These values are currently only stored in memory, and will be used in a future revision.

Example: `sudo python3 pixels.py -i image.png -q 2`

The following options are available via CLI:

| Flags      | Description |
| ----------- | ----------- |
| `-i`, `--source` | Name of file to be resized and striped |
| `-s`, `--size` | Width/Height to resize image to, in pixels |
| `-q`, `--jpeg` | Set the output JPEG quality level. Defaults to 95 |

> **Warning**: Setting the output quality to 100 will disable portions of the JPEG compression algorithm and may result in inflated file sizes.

## Todo

- (Optional) Function to pretty-print RGB list for visual reference
- Integrate with Raspberry Pi addressable LED output