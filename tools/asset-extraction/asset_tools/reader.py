# parser.py
# thomwheeler04@vt.edu - thomaswheeler443@gmail.com
#
# Helps parse binary files
import ctypes

class ByteReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name, 'rb')
    
    # Read the next value as a single byte
    def read_byte(self):
        return self.file.read(1)
    
    # Read the next value as a short
    def read_short(self, byteorder='little'):
        bytes = self.file.read(2)
        val = int.from_bytes(bytes, byteorder=byteorder)
        return ctypes.c_ushort(val).value
    
    # Read the next value as a long
    def read_long(self, byteorder='little'):
        bytes = self.file.read(4)
        val = int.from_bytes(bytes, byteorder=byteorder)
        return ctypes.c_ulong(val).value
    
    # Read the next value as a utf8 string
    def read_string(self, num, encoding='utf-8'):
        bytes = self.file.read(num)
        try:
            str = bytes.decode(encoding)
        except:
            return "ERROR_VAL"
        return str
    
    # Skip a certain number of bytes
    def skip(self, len, whence=1):
        self.file.seek(len, whence)
    
    # Read and retrieve raw bytes
    def read_bytes(self, len):
        bytes = self.file.read(len)
        return bytes
    
    # Get the current offset
    def curr_offset(self):
        return self.file.tell()
     
    # Close parser
    def close(self):
        self.file.close()
