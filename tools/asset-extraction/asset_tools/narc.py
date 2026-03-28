# narc.py
# thomwheeler04@vt.edu - thomaswheeler443@gmail.com
#
# Instance of a 'Nitro Archive (NARC)' file

# Using documentation from http://problemkaputt.de/gbatek.htm#dscartridgenitroromandnitroarcfilesystems

from reader import ByteReader
from dataclasses import dataclass

# Dataclass for helping with File Name Tables
@dataclass
class _FNT:
    sub_table_offset: int
    first_file_id: int
    num_dir: int
    sub_parent_ids: list
    sub_tables: list

@dataclass 
class _FNTSubTable:
    type: int   # Whether 
    len: int    # Represents both type and length, depending on value
    name: str
    sub_directory_id: int   # Only present if type == 1 and len > 0

@dataclass
class _GMIF:
    name: str   # Chunk name "GMIF"
    size: int   # Chunk size
    narc_offset: int    # Data start offset

class Narc:
    def __init__(self, narc_file):
        self.file = narc_file
        self.reader = ByteReader(narc_file)
        
        # Read header info
        # See link above for details
        self.narc_name = self.reader.read_string(4)
        self.byte_order = self.reader.read_bytes(2)
        self.version = self.reader.read_short()
        self.file_size = self.reader.read_long()
        self.narc_size = self.reader.read_short()
        self.num_chunks = self.reader.read_short()
        self.reader.skip(2) # Skip for reserved bytes
        
        # Read File Allocation Table Block (BTAF)
        self.btaf_name = self.reader.read_string(4)
        self.btaf_size = self.reader.read_long()
        self.btaf_num_files = self.reader.read_short()
        self.fat = self._read_fat(self.btaf_num_files)
        
        # Read File Name Table Block (BTNF)
        self.btnf_name = self.reader.read_string(4)
        self.btnf_size = self.reader.read_long()
        self.fnt = self._read_fnt()
        
        # Get padding
        self.padding = self._get_pad()
        
        # Files within archive
        self.chunks = self._read_chunks()
        
    # Helper to help read FAT (File Allocation Table)
    def _read_fat(self, num_files):
        fat = []
        for i in range(num_files):
            start = self.reader.read_long()
            end = self.reader.read_long()
            fat.append((start, end))
        return fat
    
    # Helper to help read FNT (File Name Table)
    def _read_fnt(self, size):
        pass
    
    def _get_pad(self):
        curr_pos = self.reader.curr_offset()
        num_bytes = (4 - (curr_pos % 4)) % 4
        return self.reader.read_bytes(num_bytes)
    
    def _read_chunks(self, num_chunks):
        pass