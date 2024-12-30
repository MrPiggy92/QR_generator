#!/usr/bin/env python3
"""
A program to calculate the best mask pattern and apply it to a QR code
"""
def mask(qr):
    return apply_mask(qr, 0)

def apply_mask(qr, mask):
    new_qr = [[-1 for _ in range(len(qr))] for _ in range(len(qr))]
    for row in range(len(qr)):
        for column in range(len(qr)):
            new_bit = masks[mask](row, column)
            new_bit = 1 - qr[row][column] if new_bit else qr[row][column]
            if new_bit == 2:
                new_bit = -1
            new_qr[row][column] = new_bit
    return new_qr

def mask0(row, column):
    return (row + column) % 2 == 0
def mask1(row, column):
    return row % 2 == 0
def mask2(row, column):
    return column % 2 == 0
def mask3(row, column):
    return (row + column) % 3 == 0
def mask4(row, column):
    return ((row//2) + (column//3)) % 2 == 0
def mask5(row, column):
    return ((row * column) % 2) + ((row * column) % 3) == 0
def mask6(row, column):
    return ( ((row * column) % 2) + ((row * column) % 3) ) % 2 == 0
def mask7(row, column):
    return ( ((row + column) % 2) + ((row * column) % 3) ) % 2 == 0

masks = [mask0, mask1, mask2, mask3, mask4, mask5, mask6, mask7]