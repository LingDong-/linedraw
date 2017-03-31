# linedraw
Convert images to vectorized line drawings for plotters.
![Alt text](/screenshots/1.png?raw=true "")

## Dependencies
Python 2, PIL/Pillow, numpy, OpenCV (Optional for better speed and results)

## Usage
Convert an image to line drawing and export .SVG format:
```shell
$ python linedraw.py -i input.jpg -o output.svg
```
Command specs:
```
usage: linedraw.py [-h] [-i [INPUT_PATH]] [-o [OUTPUT_PATH]] [-b] [-nc] [-nh]
                   [--no_cv] [--hatch_size [HATCH_SIZE]]
                   [--contour_simplify [CONTOUR_SIMPLIFY]]

Convert image to vectorized line drawing for plotters.

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUT_PATH], --input [INPUT_PATH]
                        Input path
  -o [OUTPUT_PATH], --output [OUTPUT_PATH]
                        Output path.
  -b, --show_bitmap     Display bitmap preview.
  -nc, --no_contour     Don't draw contours.
  -nh, --no_hatch       Disable hatching.
  --no_cv               Don't use openCV.
  --hatch_size [HATCH_SIZE]
                        Patch size of hatches. eg. 8, 16, 32
  --contour_simplify [CONTOUR_SIMPLIFY]
                        Level of contour simplification. eg. 1, 2, 3
```
