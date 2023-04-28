#!/usr/bin/env python3

import struct

"""Script converts .txt file to .bin file, and vice versa.

Task. Write a script to convert a file from text to binary format (for example,
you can use the struct module), and vice versa, from binary to text. Make sure 
that after converting to one side and then to the other, we get the same output
file, i.e. 
     to_text(to_binary(text)) == text and to_binary(to_text(binary)) == binary.
"""


def to_binary(text):
    binary = b''
    lines = text.strip().split('\n')
    for line in lines:
        parts = line.split(' - ')
        timestamp = parts[0].encode('utf-8')
        temperature = float(parts[1])
        binary += struct.pack('!I', len(timestamp))
        binary += timestamp
        binary += struct.pack('!d', temperature)
    return binary

def to_text(binary):
    text = ''
    pos = 0
    while pos < len(binary):
        length = struct.unpack('!I', binary[pos:pos+4])[0]
        pos += 4
        timestamp = binary[pos:pos+length].decode('utf-8')
        pos += length
        temperature = struct.unpack('!d', binary[pos:pos+8])[0]
        pos += 8
        text += f'{timestamp} - {temperature:.1f}\n'
    return text


if __name__ == '__main__':

    filename = 'templog.txt'
    with open(filename, 'r') as f:
        text = f.read()
    print('\nContents of ' + '\033[1m' + f'{filename}' + '\033[0m' +':')
    print(text)

    # Convert text to binary
    binary = to_binary(text)
    with open(f'{filename}.bin', 'wb') as f:
        f.write(binary)

    with open(f'{filename}.bin', 'rb') as f:
        binary = f.read()
    print('Contents of ' + '\033[1m' + f'{filename}.bin' + '\033[0m' +':')
    print(binary)

    # Convert binary back to text
    text = to_text(binary)
    with open(f'{filename}.txt', 'w') as f:
        f.write(text)

    # Verify that the original text and the final text are the same
    with open(filename, 'r') as f:
        original_text = f.read()
    with open(f'{filename}.txt', 'r') as f:
        final_text = f.read()
    print('\nContents of ' + '\033[1m' + f'{filename}.txt' + '\033[0m' +':')
    print(final_text)
    
    if original_text == final_text:
        print("Conversion successful!\n")
    else:
        print("Conversion failed!\n")

