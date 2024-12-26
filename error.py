#!/usr/bin/env python3
"""
A program to generate Reed-Solomon error codewords for a piece of data
"""

#-- IMPORTS --#
import copy

#-- CONSTANTS --#
# These convert a^x to int and int to a^x
int_to_exponent = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 29: 8, 58: 9, 116: 10, 232: 11, 205: 12, 135: 13, 19: 14, 38: 15, 76: 16, 152: 17, 45: 18, 90: 19, 180: 20, 117: 21, 234: 22, 201: 23, 143: 24, 3: 25, 6: 26, 12: 27, 24: 28, 48: 29, 96: 30, 192: 31, 157: 32, 39: 33, 78: 34, 156: 35, 37: 36, 74: 37, 148: 38, 53: 39, 106: 40, 212: 41, 181: 42, 119: 43, 238: 44, 193: 45, 159: 46, 35: 47, 70: 48, 140: 49, 5: 50, 10: 51, 20: 52, 40: 53, 80: 54, 160: 55, 93: 56, 186: 57, 105: 58, 210: 59, 185: 60, 111: 61, 222: 62, 161: 63, 95: 64, 190: 65, 97: 66, 194: 67, 153: 68, 47: 69, 94: 70, 188: 71, 101: 72, 202: 73, 137: 74, 15: 75, 30: 76, 60: 77, 120: 78, 240: 79, 253: 80, 231: 81, 211: 82, 187: 83, 107: 84, 214: 85, 177: 86, 127: 87, 254: 88, 225: 89, 223: 90, 163: 91, 91: 92, 182: 93, 113: 94, 226: 95, 217: 96, 175: 97, 67: 98, 134: 99, 17: 100, 34: 101, 68: 102, 136: 103, 13: 104, 26: 105, 52: 106, 104: 107, 208: 108, 189: 109, 103: 110, 206: 111, 129: 112, 31: 113, 62: 114, 124: 115, 248: 116, 237: 117, 199: 118, 147: 119, 59: 120, 118: 121, 236: 122, 197: 123, 151: 124, 51: 125, 102: 126, 204: 127, 133: 128, 23: 129, 46: 130, 92: 131, 184: 132, 109: 133, 218: 134, 169: 135, 79: 136, 158: 137, 33: 138, 66: 139, 132: 140, 21: 141, 42: 142, 84: 143, 168: 144, 77: 145, 154: 146, 41: 147, 82: 148, 164: 149, 85: 150, 170: 151, 73: 152, 146: 153, 57: 154, 114: 155, 228: 156, 213: 157, 183: 158, 115: 159, 230: 160, 209: 161, 191: 162, 99: 163, 198: 164, 145: 165, 63: 166, 126: 167, 252: 168, 229: 169, 215: 170, 179: 171, 123: 172, 246: 173, 241: 174, 255: 175, 227: 176, 219: 177, 171: 178, 75: 179, 150: 180, 49: 181, 98: 182, 196: 183, 149: 184, 55: 185, 110: 186, 220: 187, 165: 188, 87: 189, 174: 190, 65: 191, 130: 192, 25: 193, 50: 194, 100: 195, 200: 196, 141: 197, 7: 198, 14: 199, 28: 200, 56: 201, 112: 202, 224: 203, 221: 204, 167: 205, 83: 206, 166: 207, 81: 208, 162: 209, 89: 210, 178: 211, 121: 212, 242: 213, 249: 214, 239: 215, 195: 216, 155: 217, 43: 218, 86: 219, 172: 220, 69: 221, 138: 222, 9: 223, 18: 224, 36: 225, 72: 226, 144: 227, 61: 228, 122: 229, 244: 230, 245: 231, 247: 232, 243: 233, 251: 234, 235: 235, 203: 236, 139: 237, 11: 238, 22: 239, 44: 240, 88: 241, 176: 242, 125: 243, 250: 244, 233: 245, 207: 246, 131: 247, 27: 248, 54: 249, 108: 250, 216: 251, 173: 252, 71: 253, 142: 254, 0: None}
exp_to_int = {0: 1, 1: 2, 2: 4, 3: 8, 4: 16, 5: 32, 6: 64, 7: 128, 8: 29, 9: 58, 10: 116, 11: 232, 12: 205, 13: 135, 14: 19, 15: 38, 16: 76, 17: 152, 18: 45, 19: 90, 20: 180, 21: 117, 22: 234, 23: 201, 24: 143, 25: 3, 26: 6, 27: 12, 28: 24, 29: 48, 30: 96, 31: 192, 32: 157, 33: 39, 34: 78, 35: 156, 36: 37, 37: 74, 38: 148, 39: 53, 40: 106, 41: 212, 42: 181, 43: 119, 44: 238, 45: 193, 46: 159, 47: 35, 48: 70, 49: 140, 50: 5, 51: 10, 52: 20, 53: 40, 54: 80, 55: 160, 56: 93, 57: 186, 58: 105, 59: 210, 60: 185, 61: 111, 62: 222, 63: 161, 64: 95, 65: 190, 66: 97, 67: 194, 68: 153, 69: 47, 70: 94, 71: 188, 72: 101, 73: 202, 74: 137, 75: 15, 76: 30, 77: 60, 78: 120, 79: 240, 80: 253, 81: 231, 82: 211, 83: 187, 84: 107, 85: 214, 86: 177, 87: 127, 88: 254, 89: 225, 90: 223, 91: 163, 92: 91, 93: 182, 94: 113, 95: 226, 96: 217, 97: 175, 98: 67, 99: 134, 100: 17, 101: 34, 102: 68, 103: 136, 104: 13, 105: 26, 106: 52, 107: 104, 108: 208, 109: 189, 110: 103, 111: 206, 112: 129, 113: 31, 114: 62, 115: 124, 116: 248, 117: 237, 118: 199, 119: 147, 120: 59, 121: 118, 122: 236, 123: 197, 124: 151, 125: 51, 126: 102, 127: 204, 128: 133, 129: 23, 130: 46, 131: 92, 132: 184, 133: 109, 134: 218, 135: 169, 136: 79, 137: 158, 138: 33, 139: 66, 140: 132, 141: 21, 142: 42, 143: 84, 144: 168, 145: 77, 146: 154, 147: 41, 148: 82, 149: 164, 150: 85, 151: 170, 152: 73, 153: 146, 154: 57, 155: 114, 156: 228, 157: 213, 158: 183, 159: 115, 160: 230, 161: 209, 162: 191, 163: 99, 164: 198, 165: 145, 166: 63, 167: 126, 168: 252, 169: 229, 170: 215, 171: 179, 172: 123, 173: 246, 174: 241, 175: 255, 176: 227, 177: 219, 178: 171, 179: 75, 180: 150, 181: 49, 182: 98, 183: 196, 184: 149, 185: 55, 186: 110, 187: 220, 188: 165, 189: 87, 190: 174, 191: 65, 192: 130, 193: 25, 194: 50, 195: 100, 196: 200, 197: 141, 198: 7, 199: 14, 200: 28, 201: 56, 202: 112, 203: 224, 204: 221, 205: 167, 206: 83, 207: 166, 208: 81, 209: 162, 210: 89, 211: 178, 212: 121, 213: 242, 214: 249, 215: 239, 216: 195, 217: 155, 218: 43, 219: 86, 220: 172, 221: 69, 222: 138, 223: 9, 224: 18, 225: 36, 226: 72, 227: 144, 228: 61, 229: 122, 230: 244, 231: 245, 232: 247, 233: 243, 234: 251, 235: 235, 236: 203, 237: 139, 238: 11, 239: 22, 240: 44, 241: 88, 242: 176, 243: 125, 244: 250, 245: 233, 246: 207, 247: 131, 248: 27, 249: 54, 250: 108, 251: 216, 252: 173, 253: 71, 254: 142, 255: 1}

#-- FUNCTIONS --#
def correction(binary_data_string):
    """
    Main function to generate codewords
    """
    # Split data into codewords
    data_codewords = []
    codeword = ""
    for bit in binary_data_string:
        codeword += str(bit)
        if len(codeword) == 8:
            data_codewords.append(int(codeword))
            codeword = ""
    # Split codewords into blocks
    block_length = int(len(data_codewords) / 2)
    block1 = data_codewords[:block_length]
    block2 = data_codewords[block_length:]
    # Convert blocks to int
    block1_int = [int(str(byte), 2) for byte in block1]
    block2_int = [int(str(byte), 2) for byte in block2]
    # Generate polynomial for block 1
    block1_poly = ""
    exponent = 42
    for num in block1_int:
        block1_poly += f"{num}x{exponent} + "
        exponent -= 1
    block1_poly = block1_poly[:-3]
    # generate polynomial for block 2
    block2_poly = ""
    exponent = 42
    for num in block2_int:
        block2_poly += f"{num}x{exponent} + "
        exponent -= 1
    block2_poly = block2_poly[:-3]
    # Define generator polynomial
    generator = "a0x24 + ɑ229x23 + ɑ121x22 + ɑ135x21 + ɑ48x20 + ɑ211x19 + ɑ117x18 + ɑ251x17 + ɑ126x16 + ɑ159x15 + ɑ180x14 + ɑ169x13 + ɑ152x12 + ɑ192x11 + ɑ226x10 + ɑ228x9 + ɑ218x8 + ɑ111x7 + ɑ0x6 + ɑ117x5 + ɑ232x4 + ɑ87x3 + ɑ96x2 + ɑ227x + ɑ21"
    # calculate and return
    return divide(block1_poly, generator), divide(block2_poly, generator)

def prepare(message, generator):
    """
    A function to prepare polynomials for division
    """
    # Split message polynomial into list of terms
    message_list = message.split(" + ")
    message_list_split = []
    for term in message_list:
        new_dict = {"int": int(term[:term.index('x')]), 'a': int_to_exponent[int(term[:term.index('x')])], 'x': int(term[term.index('x')+1:])}
        message_list_split.append(new_dict)
    # Split generator polynomial into list of terms
    generator_list = generator.split(" + ")
    generator_list_split = []
    for term in generator_list:
        if term[-1] == 'x':
            new_dict = {"int": exp_to_int[int(term[1:-1])], 'a': int(term[1:-1]), 'x': 1}
        elif 'x' in term:
            new_dict = {"int": exp_to_int[int(term[1:term.index('x')])], 'a': int(term[1:term.index('x')]), 'x': int(term[term.index('x')+1:])}
        else:
            new_dict = {"int": exp_to_int[int(term[1:])], 'a': int(term[1:]), 'x': 0}
        generator_list_split.append(new_dict)
    # Multiply polynomials so exponents dont get too small
    for term in message_list_split:
        term['x'] += 24
    wanted_exponent = message_list_split[0]['x']
    required_increase = wanted_exponent - generator_list_split[0]['x']
    # Multiply generator so exponent of x is equal to message
    for term in generator_list_split:
        term['x'] += required_increase
    return message_list_split, generator_list_split

def divide(message, generator):
    """
    A function to divide polynomials
    """
    # prepare polynomials
    message_list_split, generator_list_split = prepare(message, generator)
    # Duplicate generator
    generator_list_split_copy = copy.deepcopy(generator_list_split)
    
    # Repeat division steps
    for x in range(len(message_list_split)):
        # If first term has coefficent of 0, remove it and skip to next step
        if message_list_split[0]['int'] == 0:
            message_list_split.pop(0)
            continue
        # Reset generator to original
        generator_list_split = copy.deepcopy(generator_list_split_copy)
        # Get a^x of first message term
        lead_alpha_exp = message_list_split[0]['a']
        # Iterate over generator terms
        for term in generator_list_split:
            # Multiply by lead_alpha_exp
            term['a'] += lead_alpha_exp # Multipling a^x and a^y == a^(x+y)
            if term['a'] > 255: # If exponent is greater than 255, mod 255
                term['a'] = term['a'] % 255
            term['int'] = exp_to_int[term['a']] # Convert a^x to int
        
        # Pad message list with 0x^y where y decreases each term
        y = message_list_split[-1]['x']
        for i in range(len(generator_list_split), len(message_list_split), -1):
            y -= 1
            message_list_split += [{"int": 0, 'x': y}]
        # Iterate over message and generator
        for mterm, gterm in zip(message_list_split, generator_list_split):
            mterm["int"] = mterm["int"] ^ gterm["int"] # XOR coefficients
            mterm['a'] = int_to_exponent[mterm["int"]] # Convert int to a^x
        # Remove lead term with coefficent of 0
        if message_list_split[0]['int'] == 0:
            message_list_split.pop(0)
    # Turn polynomials into list of ints
    coefficients = [term["int"] for term in message_list_split]
    return coefficients
    


# 1 group
# 2 blocks
# 43 data codewords / block
# 24 error correction codewords / block
# 64,86,134,86,198,198,240,236,17,236,17,236,17,236,17,236,17,236,17,236,17,236,17,236,17,236,17,236,17,236,17,236,17,236,17,236,17,236,17,236,17,236,17

# generator polynomial
# ɑ0x24 + ɑ229x23 + ɑ121x22 + ɑ135x21 + ɑ48x20 + ɑ211x19 + ɑ117x18 + ɑ251x17 + ɑ126x16 + ɑ159x15 + ɑ180x14 + ɑ169x13 + ɑ152x12 + ɑ192x11 + ɑ226x10 + ɑ228x9 + ɑ218x8 + ɑ111x7 + ɑ0x6 + ɑ117x5 + ɑ232x4 + ɑ87x3 + ɑ96x2 + ɑ227x + ɑ21

#-- MAIN --#
if __name__ == "__main__":
    print(correction([0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0]))
