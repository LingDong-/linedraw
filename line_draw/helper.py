from PIL import Image, ImageOps, ImageDraw
import line_draw.perlin as perlin
from datetime import datetime
import os

from line_draw.filters import appmask, F_SobelX, F_SobelY
from line_draw.default import argument
from line_draw.util import distsum, is_image_file, extract_file_name_and_extension
from line_draw.strokesort import sortlines


def sketch(input_path, output_path:str):
    IMAGE = None

    if not is_image_file(input_path):
        return print("Please provide the path for an image.")

    out_file, out_ext = extract_file_name_and_extension(output_path)

    if not out_file:
        in_file, in_ext = extract_file_name_and_extension(input_path)
        out_ext = '.svg'
        if not output_path.endswith('/'):
            output_path += '/'
        output_path += in_file + out_ext

    if out_ext != '.svg':
         return print("Currently we can only save as svg file")

    try:
        IMAGE = Image.open(input_path)
    except FileNotFoundError:
        return print("The Input File wasn't found. Check Path")

    width, height = IMAGE.size

    IMAGE = IMAGE.convert("L")
    IMAGE = ImageOps.autocontrast(IMAGE, 10)

    lines = []

    if argument.draw_contours:
        lines += get_contours(IMAGE.resize((argument.resolution // argument.contour_simplify,
                                            argument.resolution // argument.contour_simplify * height // width)))

    if argument.draw_hatch:
        lines += hatch(IMAGE.resize(
            (argument.resolution // argument.hatch_size, argument.resolution // argument.hatch_size * height // width)))

    lines = sortlines(lines)

    if argument.show_bitmap:
        disp = Image.new("RGB", (argument.resolution, argument.resolution * height // width), (255, 255, 255))
        draw = ImageDraw.Draw(disp)
        for l in lines:
            draw.line(l, (0, 0, 0), 5)
        disp.show()

    # if out_ext != '.svg':
    #     now = datetime.now()
    #     svg_path = output_path.rsplit('/', 1)[0] + now.strftime("%Y%m%d%H%M%S%f") + '.svg'
    # else:
    #     svg_path = output_path

    file = open(output_path, 'w')
    file.write(make_svg(lines))
    file.close()

    # if out_ext != '.svg':
    #     if not is_image_file(output_path):
    #         return "Output path is not an image path"
    #     rasterise_image(svg_path,output_path)
    #     os.remove(svg_path)
    print(len(lines), "strokes.")
    if argument.save_settings:
        argument.save(os.path.dirname(output_path) + '/settings.json')
    print("done.")
    return lines


def get_contours(image):
    print("Generating Contours....")
    image = find_edges(image)
    image_copy1 = image.copy()
    image_copy2 = image.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    image_copy1_dots = get_dots(image_copy1)
    image_copy1_contours = connect_dots(image_copy1_dots)
    image_copy2_dots = get_dots(image_copy2)
    image_copy2_contours = connect_dots(image_copy2_dots)

    for i in range(len(image_copy2_contours)):
        image_copy2_contours[1] = [(c[1], c[0]) for c in image_copy2_contours[i]]
    contours = image_copy1_contours + image_copy2_contours

    for i in range(len(contours)):
        for j in range(len(contours)):
            if len(contours[i]) > 0 and len(contours[j]) > 0:
                if distsum(contours[j][0], contours[i][-1]) < 8:
                    contours[i] = contours[i] + contours[j]
                    contours[j] = []

    for i in range(len(contours)):
        contours[i] = [contours[i][j] for j in range(0, len(contours[i]), 8)]

    contours = [c for c in contours if len(c) > 1]

    for i in range(0, len(contours)):
        contours[i] = [(v[0] * argument.contour_simplify, v[1] * argument.contour_simplify) for v in contours[i]]

    for i in range(0, len(contours)):
        for j in range(0, len(contours[i])):
            contours[i][j] = int(contours[i][j][0] + 10 * perlin.noise(i * 0.5, j * 0.1, 1)), int(
                contours[i][j][1] + 10 * perlin.noise(i * 0.5, j * 0.1, 2))

    return contours


def find_edges(image):
    print("Fining Edges....")
    if argument.no_cv:
        appmask(image, [F_SobelX, F_SobelY])
    else:
        import numpy as np
        import cv2
        image = np.array(image)
        image = cv2.GaussianBlur(image, (3, 3), 0)
        image = cv2.Canny(image, 100, 200)
        image = Image.fromarray(image)
    return image.point(lambda p: p > 128 and 255)


def get_dots(image):
    print("Getting contour points...")
    PX = image.load()
    dots = []
    width, height = image.size
    for y in range(height - 1):
        row = []
        for x in range(1, width):
            if PX[x, y] == 255:
                if len(row) > 0:
                    if x - row[-1][0] == row[-1][-1] + 1:
                        row[-1] = (row[-1][0], row[-1][-1] + 1)
                    else:
                        row.append((x, 0))
                else:
                    row.append((x, 0))
        dots.append(row)
    return dots


def connect_dots(dots):
    print("Connecting contour points....")
    contours = []
    for y in range(len(dots)):
        for x, v in dots[y]:
            if v > -1:
                if y == 0:
                    contours.append([(x, y)])
                else:
                    closest = -1
                    cdist = 100
                    for x0, v0 in dots[y - 1]:
                        if abs(x0 - x) < cdist:
                            cdist = abs(x0 - x)
                            closest = x0
                    if cdist > 3:
                        contours.append([(x, y)])
                    else:
                        found = 0
                        for i in range(len(contours)):
                            if contours[i][-1] == (closest, y - 1):
                                contours[i].append((x, y,))
                                found = 1
                                break
                        if found == 0:
                            contours.append([(x, y)])
        for c in contours:
            if c[-1][1] < y - 1 and len(c) < 4:
                contours.remove(c)
    return contours


def hatch(image):
    print("Hatching....")
    PX = image.load()
    width, height = image.size
    lg1 = []
    lg2 = []
    for x0 in range(width):
        for y0 in range(height):
            x = x0 * argument.hatch_size
            y = y0 * argument.hatch_size
            if PX[x0, y0] > 144:
                pass
            elif PX[x0, y0] > 64:
                lg1.append([(x, y + argument.hatch_size / 4), (x + argument.hatch_size, y + argument.hatch_size / 4)])
            elif PX[x0, y0] > 16:
                lg1.append([(x, y + argument.hatch_size / 4), (x + argument.hatch_size, y + argument.hatch_size / 4)])
                lg2.append([(x + argument.hatch_size, y), (x, y + argument.hatch_size)])
            else:
                lg1.append([(x, y + argument.hatch_size / 4), (x + argument.hatch_size, y + argument.hatch_size / 4)])
                lg1.append([(x, y + argument.hatch_size / 2 + argument.hatch_size / 4),
                            (x + argument.hatch_size, y + argument.hatch_size / 2 + argument.hatch_size / 4)])
                lg2.append([(x + argument.hatch_size, y), (x, y + argument.hatch_size)])
    lines = [lg1, lg2]
    for k in range(0, len(lines)):
        for i in range(0, len(lines[k])):
            for j in range(0, len(lines[k])):
                if lines[k][i] != [] and lines[k][j] != []:
                    if lines[k][i][-1] == lines[k][j][0]:
                        lines[k][i] = lines[k][i] + lines[k][j][1:]
                        lines[k][j] = []
        lines[k] = [l for l in lines[k] if len(l) > 0]
    lines = lines[0] + lines[1]
    for i in range(0, len(lines)):
        for j in range(0, len(lines[i])):
            lines[i][j] = int(lines[i][j][0] + argument.hatch_size * perlin.noise(i * 0.5, j * 0.1, 1)), int(
                lines[i][j][1] + argument.hatch_size * perlin.noise(i * 0.5, j * 0.1, 2)) - j
    return lines


def make_svg(lines):
    print("Generating SVG file....")
    out = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">'
    for l in lines:
        l = ",".join([str(p[0] * 0.5) + "," + str(p[1] * 0.5) for p in l])
        out += '<polyline points="' + l + '" stroke="black" stroke-width="2" fill="none" />\n'
    out += '</svg>'
    return out


def rasterise_image(svg_image, raster_image):
    print("Converting image....")
    # to be implemented
