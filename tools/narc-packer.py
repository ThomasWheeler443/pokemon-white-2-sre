#
# narc-packer.py
# thomaswheeler443@gmail.com - thomwheeler04@vt.edu
#
# Pack a group of files into a NARC file

import os
import sys
from pathlib import Path

class NarcBuffer(bytearray):

    # Add placeholder data and 
    # return the offset to said data
    def placeholder(self, size):
        offset = len(self)
        for i in range(size):
            self.extend(b'\xAA')
        return offset

    # Write bytes at offset
    # For use with placeholders
    def write_data(self, offset, data: bytearray):
        for i, b in enumerate(data):
            self[offset + i] = b

    def write_int(self, offset, num, int_size):
        self.write_data(offset, num.to_bytes(int_size, byteorder='little'))

def main():

    if len(sys.argv) != 3:
        print(f"Incorrect number of arguments!")
        print(f"USEAGE: python narc-packer.py <INPUT DIR> <OUT FILE>")
        exit(1)

    # Input Dir walk
    in_walk = os.walk(sys.argv[1])

    # Output narc buffer
    narc_buff = NarcBuffer()

    # Documentation from https://problemkaputt.de/gbatek.htm#dscartridgenitroromandnitroarcfilesystems

    print(f"Creating NARC Headers...")


    # =======================
    # NARC Header
    # =======================  
    narc_buff.extend(b'NARC')       # NARC Magic
    narc_buff.extend(b'\xFE\xFF')   # Byte Order (always 0xFFFE)
    narc_buff.extend(b'\x00\x01')   # Version (always 0x0100)

    file_size_ph = narc_buff.placeholder(4)

    narc_buff.extend(b'\x10\x00')   # Narc Chunk Size (always 0x0010)
    narc_buff.extend(b'\x03\x00')   # Number of following chunks (always 0x0003)


    # =======================
    # File Allocation Table
    # =======================
    fat_start = len(narc_buff)

    narc_buff.extend(b'BTAF')       # BTAF Magic

    fat_size_ph = narc_buff.placeholder(4)
    num_files_ph = narc_buff.placeholder(2)

    narc_buff.extend(b'\x00\x00')   # Reserved Padding

    # Loop through files and get place
    file_list = {}
    for root, dirs, files in in_walk:
        for file in sorted(files):
            if file == "narc_info.txt":
                continue
            fa = narc_buff.placeholder(8)
            file_list[root+file] = fa       # Include root for files with same name
    
    # Write back to placeholders
    narc_buff.write_int(fat_size_ph, len(narc_buff) - fat_start, 4)
    narc_buff.write_int(num_files_ph, len(file_list), 2)


    # =======================
    # File Name Table
    # =======================
    
    fnt_base = len(narc_buff)
    narc_buff.extend(b'BTNF')               # BTNF Magic

    # For now, we assume all files are nameless in the narc

    narc_buff.extend(b'\x10\x00\x00\x00')   # Offset to Sub-table (In this case, to GMIF)
    narc_buff.extend(b'\x04\x00')           # ID of first file in subtable
    narc_buff.extend(b'\x00\x00')           # Number of Directories

    narc_buff.extend(b'\x00\x00\x01\x00')   # Unknown (likely for nameless fnt)

    # Non-nameless Implementation:
    # fnt_main_list = {}
    # for root, dirs, files in in_walk:
    #     main_table = narc_buff.placeholder(8)
    #     fnt_main_list[root] = main_table

    # for key, value in fnt_main_list.items()
    #     narc_buff.write_int()
    

    # =======================
    # File Images
    # =======================
    
    narc_buff.extend(b'GMIF')               # GMIF Magic
    
    img_size_ph = narc_buff.placeholder(4)

    img_base = len(narc_buff)

    # Loop through files
    for file_str, fat_pos in sorted(file_list.items()):

        print(f"Writing {file_str} to Nitro Archive..")

        file_base = len(narc_buff)
        
        # Append file contents to buffer
        with open(file_str, 'rb') as f:
            data = f.read()
        narc_buff.extend(data)              # IMG file Data

        # Add info to file allocation table
        narc_buff.write_int(fat_pos, file_base - img_base, 4)
        narc_buff.write_int(fat_pos + 4, len(narc_buff) - img_base, 4)

    # Add sizes
    narc_buff.write_int(img_size_ph, len(narc_buff) - img_base + 8, 4) 
    narc_buff.write_int(file_size_ph, len(narc_buff), 4)

    # Pad tt 4 bits
    while (len(narc_buff) % 4) != 0:
        narc_buff.extend(b'\x00')

    print(f"Writing contents to {sys.argv[2]}...")

    # Write buffer to output
    with open(sys.argv[2], 'wb') as f:
        f.write(narc_buff)

    print(f"Created Nitro Archive at {sys.argv[2]}")


if __name__ == "__main__":
    main()
    exit(0)
