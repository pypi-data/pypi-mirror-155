#!/usr/bin/env python3

import click
from PIL import Image
from PIL import ImageOps


@click.command()
@click.argument("FILENAME")
@click.argument("SIZE", nargs=-1)
def cli(filename, size):
    if not size:
        size = (16, 32, 48, 128)
    else:
        size = [int(x) for x in size]

    src_image = Image.open(filename, "r")

    for size in size:
        icon = src_image.resize((size, size), Image.LANCZOS)
        icon.save("icon{size}.png".format(size=size))
        if size == 19:
            grayscale_icon = ImageOps.grayscale(icon)
            grayscale_icon.save("icon{size}-disable.png".format(size=size))


if __name__ == "__main__":
    cli()
