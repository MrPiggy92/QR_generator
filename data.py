#!/usr/bin/env python3
"""
A program to encode data into ISO 8859-1
"""

#-- CONSTANTS --#
char_set = {
    chr(i): format(i, '08b') for i in range(256) # A dictionary mapping characters to their equivalent binary codes.
}

#-- FUNCTIONS --#
def str_to_bin(data_string):
    """
    A function to convert a string to a list of bits
    """
    binary_data_string = [] # Initialise the list
    for char in data_string: # Iterate over the string
        for bit in char_set[char]: # Iterate over the encoded byte
            binary_data_string.append(int(bit)) # Append the bit (as an int) to the list
    return binary_data_string

def encode(data_string):
    """
    A function to fully encode data for QR codes
    """
    if len(data_string) > 84: # Check if data is too long
        raise RuntimeError("Data too long") # Raise error
    binary_data_string = [] # Initialise list
    for bit in "0100": # Iterate over mode nibble
        binary_data_string.append(int(bit)) # Append bit (as int) to list
    for bit in format(len(data_string), "08b"): # Iterate over binary code for data length
        binary_data_string.append(int(bit)) # Append bit (as int) to list
    binary_data_string += str_to_bin(data_string) # Append encoded data
    
    if len(binary_data_string) < 688 and len(binary_data_string) > 683: # Check if data is nearly long enough
        while len(binary_data_string) < 688:
            binary_data_string.append(0) # Add 0s until long enough
    elif len(binary_data_string) < 688: # If data is not long enough
        for _ in range(4): # Add 4 0s to the end
            binary_data_string.append(0)
        while len(binary_data_string) % 8 != 0: # Add 0s until the string can be split into bytes
            binary_data_string.append(0)
        first = True
        while len(binary_data_string) < 688: # Repeat until string is long enough
            pad_string = format(236 if first else 17, "08b") # Add binary for either 236 or 17 to the end
            for bit in pad_string:
                binary_data_string.append(int(bit))
            first = not first # Next time, change if it's 236 or 17
    
    return binary_data_string
    
#-- MAIN --#
if __name__ == "__main__":
    print(encode(input(" > ")))
