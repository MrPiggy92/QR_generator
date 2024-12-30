#!/usr/bin/env python3
"""
A program to generate QR codes
"""

#-- IMPORTS --#
import data
import error
import structure
import placement
import masks
#import formatting
import render

#-- FUNCTIONS --#
def generate_QR(data_string):
    binary_data_string = data.encode(data_string) # Encode data with ISO 8859-1
    dec_error_string = error.correction(binary_data_string) # Get Reed-Solomon error codewords for encoded data
    #return dec_error_string
    full_string = structure.structure(binary_data_string, dec_error_string)
    layout = placement.place(full_string)
    masked = masks.mask(layout)
    render.render(masked)
    return masked
    #return binary_error_string

#-- MAIN --#
if __name__ == "__main__":
    print(generate_QR(input(" > ")))
