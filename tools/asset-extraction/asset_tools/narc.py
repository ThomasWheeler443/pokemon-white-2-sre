# narc.py
# thomwheeler04@vt.edu - thomaswheeler443@gmail.com
#
# Instance of a 'Nitro Archive (NARC)' file

# Using documentation from http://problemkaputt.de/gbatek.htm#dscartridgenitroromandnitroarcfilesystems

import os
from asset_tools.reader import ByteReader
from asset_tools.formats import Magic, Magic_ID
from asset_tools.raw import RawFile
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path

# Dataclass for helping with File Name Tables
@dataclass
class _FNT:
    sub_table_offset: int = -1
    first_file_id: int = -1
    num_dir: int = -1
    sub_parent_id: int = -1
    sub_tables: list[_FNTSubTable] = field(default_factory=list)

class FNT_ST_Type(Enum):
    FILE_ENTRY = 0
    SUB_DIR_ENTRY = 1
    SUB_TABLE_END = 2
    RESERVED = 3

@dataclass 
class _FNTSubTable:
    type: int = -1   # Whether 
    len: int = -1    # Represents both type and length, depending on value
    name: str = ""
    sub_dir_id: int = -1   # Only present if type == 1 and len > 0

@dataclass
class _GMIF:
    name: str   # Chunk name "GMIF"
    size: int   # Chunk size
    narc_offset: int    # Data start offset

class Narc():
    def __init__(self, narc_file, out_dir):
        self.file = narc_file
        self.reader = ByteReader(narc_file)
        self.out_dir = out_dir + os.sep
        Path(self.out_dir).mkdir(parents=True, exist_ok=True)
        
        # Read header info
        # See link above for details
        self.narc_magic = self.reader.read_string(4)
        
        if self.narc_magic != "NARC":
            print(f"File is not a NARC file!")
            exit(1)
            
        self.byte_order = self.reader.read_bytes(2)
        ver_minor = self.reader.read_byte()
        ver_major = self.reader.read_byte()
        self.version = (ver_major, ver_minor)
        self.file_size = self.reader.read_long()
        
        self.narc_size = self.reader.read_short()
        self.num_chunks = self.reader.read_short()
        #self.reader.skip(2)
        
        # Read File Allocation Table Block (BTAF)
        self.btaf_magic = self.reader.read_string(4)
        self.btaf_size = self.reader.read_long()
        self.btaf_num_files = self.reader.read_short()
        self.reader.skip(2)
        self.fat = self._read_fat(self.btaf_num_files)
        
        # Read File Name Table Block (BTNF)
        self.btnf_magic = self.reader.read_string(4)
        self.btnf_size = self.reader.read_long()
        self.fnt = self._read_fnt(first=True)
        
        # Get padding
        self.padding = self._get_pad()
        
        # get file image block
        self.gmif_name = self.reader.read_string(4)
        self.gmif_chunk_size = self.reader.read_long()
        
        # Save end
        self.image_base = self.reader.curr_offset()
        
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
    def _read_fnt(self, first=False):
        fnt = _FNT()
        fnt.sub_table_offset = self.reader.read_long()
        fnt.first_file_id = self.reader.read_short()
        if (first):
            fnt.num_dir = self.reader.read_short()
        else:
            fnt.sub_parent_id = self.reader.read_short()
        # Read sub-tables
        for i in range(fnt.num_dir-1):
            fnt.sub_tables.append(self._read_fnt_subtable())
        
        return fnt
    
    def _read_fnt_subtable(self):
        sub = _FNTSubTable()
        next = self.reader.read_byte()
        id_field = (next[0] & 0x80) >> 7
        sub.len = next[0] & 0x7f
        
        if (sub.len > 0 and not id_field):
            sub.type = FNT_ST_Type.FILE_ENTRY
            
        elif (sub.len > 0 and id_field):
            sub.type = FNT_ST_Type.SUB_DIR_ENTRY
            
        elif (sub.len == 0 and not id_field):
            sub.type = FNT_ST_Type.SUB_TABLE_END
        
        elif (sub.len == 0 and id_field):
            sub.type = FNT_ST_Type.RESERVED
        
        if (sub.len > 0):
            sub.name += self.reader.read_string(sub.len)
        
        if (sub.type == FNT_ST_Type.SUB_DIR_ENTRY):
            sub.sub_dir_id = self.reader.read_bytes(2)
            
        return sub
    
    # Helper to get any padding that my exist
    def _get_pad(self):
        curr_pos = self.reader.curr_offset()
        num_bytes = (4 - (curr_pos % 4)) % 4
        return self.reader.read_bytes(num_bytes)
    
    # Helper to help read File chunks
    def _read_chunks(self):
        chunks = []
        for fat in self.fat:
            self.reader.skip(fat[0] + self.image_base, whence=0)
            magic = self.reader.read_bytes(4)
            self.reader.skip(1)
            magic_bak = self.reader.read_bytes(4)
            chunks.append((magic, magic_bak))
        return chunks
    
    def print(self):
        # NARC
        print()
        print(f"Nitro Archive (NARC) file: {self.file}")
        print(f"  Magic (NARC): {self.narc_magic}")
        print(f"  Order Bytes: {self.byte_order}")
        print(f"  Version: {int.from_bytes(self.version[0])}.{int.from_bytes(self.version[1])}")
        print(f"  File Size: {self.file_size} bytes")
        print(f"  NARC Chunk Size: {self.narc_size} bytes")
        print(f"  Number of Following Chunks: {self.num_chunks}")
        
        # BTAF
        print()
        print(f"  File Allocation Table Block (BTAF):")
        print(f"    Magic (BTAF): {self.btaf_magic}")
        print(f"    BTAF Chunk Size: {self.btaf_size} bytes")
        print(f"    Number of Files: {self.btaf_num_files}")
        
        # Loop through File Allocation Table
        for i, entry in enumerate(self.fat):
            print()
            print(f"    FAT Entry {i+1}: ({entry[1] - entry[0]} bytes)")
            print(f"      Start Offset: +{hex(entry[0])}")
            print(f"      End Offset: +{hex(entry[1])}")
        
        # BTNF
        print()
        print(f"  File Name Table Block (BTNF):")
        print(f"    Magic (BTNF): {self.btnf_magic}")
        print(f"    BTNF Chunk Size: {self.btnf_size} bytes")
        
        # FNT
        print()
        print(f"    FNT Directory Table: ")
        print(f"      Offset to Sub-table: +{self.fnt.sub_table_offset} bytes")
        print(f"      First File ID: {self.fnt.first_file_id}")
        print(f"      Number of Directories: {self.fnt.num_dir}")
        
        # Loop through File Name Subtables
        for i, table in enumerate(self.fnt.sub_tables):
            print()
            print(f"      Sub Table:")
            print(f"        Type: {table.type}")
            print(f"        Length: {table.len}")
            print(f"        File/Dir Name: {table.name}")
            if (table.type == FNT_ST_Type.SUB_DIR_ENTRY):
                print(f"        Sub Directory ID: {table.sub_dir_id}")
            
        print(f"  Padding: {self.padding}")
        
        # Chunk size
        print()
        print(f"  File Image Block (GMIF):")
        print(f"    Magic: {self.gmif_name}")
        print(f"    Chunk Size: {hex(self.gmif_chunk_size)}")
        
        
        # Print File Data
        print()
        print(f"  Image Base: {hex(self.image_base)}")
        print(f"  Chunks:")
        for i, chunk in enumerate(self.chunks):
            name, f_type = Magic_ID(chunk[0])
            if f_type == RawFile:
                bak_name, bak_type = Magic_ID(chunk[1])
                if bak_type != RawFile:
                    name = bak_name
            print(f"    Chunk {i+1}: {name}")
            
    
    def _carve(self, fat):
        curr_pos = self.reader.curr_offset()
        self.reader.skip(fat[0] + self.image_base, whence=0)
        data = self.reader.read_bytes(fat[1] - fat[0])
        self.reader.skip(curr_pos, whence=0)
        return data
    
    def extract(self):
        for i, fat in enumerate(self.fat):
            data = self._carve(fat)
            _, file_type = Magic_ID(data[:4])
            _, backup_type = Magic_ID(data[5:9])
            if file_type == RawFile and backup_type != RawFile:
                file_type = backup_type
            if file_type == None:    
                continue
            
            file_name = f"{self.out_dir}chunk_{i+1}{file_type.ext}"
            out = file_type()
            out.create(data, file_name)
            out.extract()
    
    def close(self):
        self.reader.close();