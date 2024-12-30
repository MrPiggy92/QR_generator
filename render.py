#!/usr/bin/env python3
"""
A program to render QR codes
"""
from PIL import Image


def render(array):
    image = Image.new(mode="1", size=(len(array), len(array)), color=1)
    pixels = image.load()
    for rownum, row in enumerate(array):
        for columnnum, column in enumerate(row):
            if column == 1:
                pixels[rownum, columnnum] = 0
    image.show()