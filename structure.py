def structure(data, error):
    data_codewords = []
    codeword = ""
    for bit in data:
        codeword += str(bit)
        if len(codeword) == 8:
            data_codewords.append(int(codeword))
            codeword = ""
    data_block_length = int(len(data_codewords) / 2)
    data_block1 = data_codewords[:data_block_length]
    data_block2 = data_codewords[data_block_length:]
    data_block1_int = [int(str(byte), 2) for byte in data_block1]
    data_block2_int = [int(str(byte), 2) for byte in data_block2]
    error_block1_int = error[0]
    error_block2_int = error[1]
    full_int = []
    for x in range(data_block_length):
        full_int.append(data_block1_int[x])
        full_int.append(data_block2_int[x])
    for x in range(len(error_block1_int)):
        full_int.append(error_block1_int[x])
        full_int.append(error_block2_int[x])
    full_binary = ''.join([format(i, '08b') for i in full_int]) + "0000000"
    return full_binary
    
    
