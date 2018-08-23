import sys

from jpeg.encode import compress_image


def main():  # pragma: no cover
    import argparse
    from pyfiglet import Figlet

    # fonts from http://www.figlet.org/examples.html
    print(Figlet(font='alligator').renderText('J P E G'))
    print(Figlet(font='big').renderText('By'))
    print(Figlet(font='colossal').renderText('Meny'))
    print(Figlet(font='colossal').renderText('Baruch'))
    print(Figlet(font='colossal').renderText('L i t a l'))

    parser = argparse.ArgumentParser(
        description='Compress image by JPEG algorithm')
    parser.add_argument(
        'SRC',
        help='The relative or absolute path to image that you want to compress'
    )
    parser.add_argument(
        'DST',
        help=
        'The destinition path for compressed image. The DST may not end with file extension',
        default='result')
    parser.add_argument(
        '-s',
        '--size',
        default=8,
        type=int,
        choices=[8, 16, 32],
        help='Sub-matrix size*size. Note that The complexity is exponential')
    parser.add_argument(
        '-e', action='store_true', help='Show entropy of images')
    # parser.add_argument(
    #     '-d', action='store_true', help='Request input for attach debugger')
    args = parser.parse_args()
    # if args.d:
    #     input("Attach debugger and Enter: ")
    compress_image(args.SRC, args.DST, args.e, args.size)

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
