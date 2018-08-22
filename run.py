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
    parser.add_argument('PATH')
    parser.add_argument(
        '-e', action='store_true', help='Show entropy of images')
    parser.add_argument(
        '-d', action='store_true', help='Request input for attach debugger')
    args = parser.parse_args()
    if args.d:
        input("Attach debugger and Enter: ")
    compress_image(args.PATH, args.e)

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
