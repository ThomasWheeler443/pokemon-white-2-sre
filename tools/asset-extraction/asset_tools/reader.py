# parser.py
# thomwheeler04@vt.edu - thomaswheeler443@gmail.com
#
# Helps parse binary files

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
        return int.from_bytes(bytes, byteorder=byteorder)
    
    # Read the next value as a long
    def read_long(self, byteorder='little'):
        bytes = self.file.read(4)
        return int.from_bytes(bytes, byteorder=byteorder)
    
    # Read the next value as a utf8 string
    def read_string(self, len, encoding='utf-8'):
        bytes = self.file.read(len)
        return bytes.decode(encoding)
    
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