import argparse

from linedraw import sketch
from linedraw.default import argument

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert image to vectorized line drawing for plotters.')
    parser.add_argument('-i', '--input', dest='input_path',
                        default='lenna', action='store', nargs='?', type=str,
                        help='Input image path')

    parser.add_argument('-o', '--output', dest='output_path',
                        default=argument.export_path, action='store', nargs='?', type=str,
                        help='Output image path')

    parser.add_argument('-r', '--resolution', dest='resolution',
                        default=argument.show_bitmap, action='store_const',
                        help='Resolution of the output image')

    parser.add_argument('-b', '--show_bitmap', dest='show_bitmap',
                        const=not argument.show_bitmap, default=argument.show_bitmap, action='store_const',
                        help='Display bitmap preview.')

    parser.add_argument('-nc', '--no_contour', dest='no_contour',
                        const=argument.draw_contours, default=not argument.draw_contours, action='store_const',
                        help="Don't draw contours.")

    parser.add_argument('-nh', '--no_hatch', dest='no_hatch',
                        const=argument.draw_hatch, default=not argument.draw_hatch, action='store_const',
                        help='Disable hatching.')

    parser.add_argument('--no_cv', dest='no_cv',
                        const=not argument.no_cv, default=argument.no_cv, action='store_const',
                        help="Don't use openCV.")

    parser.add_argument('--hatch_size', dest='hatch_size',
                        default=argument.hatch_size, action='store', nargs='?', type=int,
                        help='Patch size of hatches. eg. 8, 16, 32')
    parser.add_argument('--contour_simplify', dest='contour_simplify',
                        default=argument.contour_simplify, action='store', nargs='?', type=int,
                        help='Level of contour simplification. eg. 1, 2, 3')

    args = parser.parse_args()

    input_path = args.input_path
    export_path = args.output_path
    argument.draw_hatch = not args.no_hatch
    argument.contour_simplify = not args.no_contour
    argument.hatch_size = args.hatch_size
    argument.contour_simplify = args.contour_simplify
    argument.show_bitmap = args.show_bitmap
    argument.no_cv = args.no_cv
    argument.resolution = args.resolution
    sketch(input_path, export_path)
