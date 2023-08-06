# PyIcon

A command-line utility that converts an image to several small icons.

## Installing

Install and update using `pip`:

```sh
$ pip install -U pyicon
```

## Usage

```sh
$ icon --help
Usage: icon.py [OPTIONS] FILENAME [SIZE]...

Options:
  --help  Show this message and exit.

# convert some.jpg to 128x128 and 48x48 icons.
$ icon some.jpg 128 48
```

## Reference

1. [click](https://github.com/pallets/click)
2. [chrome-extension-icon-generator](https://github.com/neglect-yp/chrome-extension-icon-generator/blob/master/icon_generator.py)