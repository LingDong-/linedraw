# linedraw
Convert images to vectorized line drawings for plotters.
![Alt text](./docs/assets/1.png?raw=true "")

- Exports polyline-only svg file with optimized stroke order for plotters;
- Sketchy style powered by Perlin noise;
- Contour-only or hatch-only modes.

## Dependencies
Python 2 or 3, PIL/Pillow, numpy, OpenCV (Optional for better performance)

```shell
pip install -r requirements.txt
```

## Usage
Convert an image to line drawing and export .SVG format:

```shell
python linedraw.py -i input.jpg -o output.svg
```
Command specs:

```
usage: linedraw.py [-h] [-i [INPUT_PATH]] [-o [OUTPUT_PATH]] [-r [RESOLUTION]] [-b] [-nc] [-nh] [--no-cv] [--hatch-size [HATCH_SIZE]] [--contour-simplify [CONTOUR_SIMPLIFY]] [-v]
                   [--save-settings]

Convert image to vectorized line drawing for plotters.

options:
  -h, --help            show this help message and exit
  -i [INPUT_PATH], --input [INPUT_PATH]
                        Input image path
  -o [OUTPUT_PATH], --output [OUTPUT_PATH]
                        Output image path
  -r [RESOLUTION], --resolution [RESOLUTION]
                        Resolution of the output image
  -b, --show-bitmap     Display bitmap preview.
  -nc, --no-contour     Don't draw contours.
  -nh, --no-hatch       Disable hatching.
  --no-cv               Don't use openCV.
  --hatch-size [HATCH_SIZE]
                        Patch size of hatches. eg. 8, 16, 32
  --contour-simplify [CONTOUR_SIMPLIFY]
                        Level of contour simplification. eg. 1, 2, 3
  -v, --visualize       Visualize the output using turtle
  --save-settings       To Save the settings to a json file

```
Python:

```python
import linedraw

linedraw.argument.resolution = 512  # set arguments
lines = linedraw.sketch("path/to/img.jpg")  # return list of polylines, eg.
# [[(x,y),(x,y),(x,y)],[(x,y),(x,y),...],...]

linedraw.visualize(lines)  # simulates plotter behavior
# draw the lines in order using turtle graphics.
```

## Future Plans
1. Rasterised Output
2. GUI for the tool