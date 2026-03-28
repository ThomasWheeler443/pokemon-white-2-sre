# narc.py
# thomwheeler04@vt.edu - thomaswheeler443@gmail.com
#
# Instance of a 'Nitro Archive (NARC)' file

# Using documentation from http://problemkaputt.de/gbatek.htm#dscartridgenitroromandnitroarcfilesystems

from reader import ByteReader

class Narc:
    def __init__(self, narc_file):
        self.file = narc_file
        
        pass
    
    