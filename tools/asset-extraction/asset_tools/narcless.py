# Narc variant for narc files without 'NARC' magic

import os
import sys
from pathlib import Path
from asset_tools.narc import Narc
from asset_tools.reader import ByteReader

class Narcless(Narc):
    def __init__(self, narc_file, out_dir):
        self.file = narc_file
        self.reader = ByteReader(narc_file)
        self.out_dir = out_dir + os.sep
        Path(self.out_dir).mkdir(parents=True, exist_ok=True)
        
        # Fill in extra data
        self.narc_magic = "N/A (narcless-narc)"
        self.byte_order = b'\x00\x00'
        self.version = (b'\x00', b'\x00')
        self.file_size = -1
        self.narc_size = -1
        self.num_chunks = -1
        
        self.padding = b''

        self.btaf_magic = "N/A (narcless-narc)"
        
        # self.btaf_num_files = self.reader.read_short()
        
        self.btnf_magic = "N/A (narcless-narc)"
        
        self.gmif_name = "N/A (narcless-narc)"
        self.gmif_chunk_size = 0

        # Get Header
        self.btnf_offset = self.reader.read_long()
        self.btnf_size = self.reader.read_long()

        self.btaf_offset = self.reader.read_long()
        self.btaf_size = self.reader.read_long()

        self.btaf_num_files = (self.btaf_size // 8)
        self.file_names = []

        self.reader.skip(self.btnf_offset, whence=0)
        self.fnt = self._read_fnt(self.reader.curr_offset())

        self.reader.skip(self.btaf_offset, whence=0)
        self.fat = self._read_fat(self.btaf_num_files)

        # Save end
        #self.image_base = self.reader.curr_offset()
        self.image_base = 0

        # Files within archive
        self.chunks = self._read_chunks()
