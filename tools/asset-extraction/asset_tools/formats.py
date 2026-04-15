# formats.py
# thomwheeler04@vt.edu - thomaswheeler443@gmail.com
#
# Define various file formats

from enum import Enum
from asset_tools.raw import RawFile

class Magic(Enum):
    NITRO_COLOR_RES = b'RLCN'
    NITRO_CHAR_GRAPHIC_RES = b'RGCN'
    NITRO_SCREEN_RES = b'RCSN'
    NITRO_FONT_RES = b'RTFN'
    NITRO_ANIM_RES = b'RNAN'
    NITRO_CELL_RES = b'RECN'
    NITRO_MULT_ANIM_RES = b'RAMN'
    NITRO_MULT_CELL_RES = b'RCMN'
    APS12_1 = b'\x20APS'
    MAP_NG = b'NG\x02\x00'
    MAP_WB = b'WB\x03\x00'
    MAP_RD = b'RD\x03\x00'
    MAP_GC = b'GC\x04\x00'
    BASIC_MODEL = b'BMD0'
    BASIC_TEXTURE = b'BTX0' 
    BASIC_CHARA_ANIM = b'BCA0'
    BASIC_TEXTURE_ANIM = b'BTA0'
    BASIC_MAT_ANIM = b'BMA0'
    BASIC_VIS_ANIM = b'BVA0'
    BASIC_TEXTURE_PAT_ANIM = b'BTP0'
    
    FILE_01 = b'\x01\x00'
    
# Classes with minimal implementation
class NitroColorRes(RawFile):
    ext = ".nclr"
    
class NitroCharGraphicRes(RawFile):
    ext = ".ncgr"
    
class NitroScreenRes(RawFile):
    ext = ".nscr"
    
class NitroFontRes(RawFile):
    ext = ".nftr"
    
class NitroAnimRes(RawFile):
    ext = ".nanr"

class NitroCellRes(RawFile):
    ext = ".ncer"
    
class NitroModelAnimRes(RawFile):
    ext = ".nmar"

class NitroModelCellRes(RawFile):
    ext = ".nmcr"
    
class APS12_1(RawFile):
    ext = ".APS12_1"
    
class MapNG(RawFile):
    ext = ".map_ng"
    
class MapWB(RawFile):
    ext = ".map_wb"
    
class MapRD(RawFile):
    ext = ".map_rd"
    
class MapGC(RawFile):
    ext = ".map_gc"
    
class BasicModel(RawFile):
    ext = ".BMD0"
    
class BasicTexture(RawFile):
    ext = ".BTX0"
    
class BasicCharAnim(RawFile):
    ext = ".BCA0"
    
class BasicTextureAnim(RawFile):
    ext = ".BTA0"
    
class BasicMaterialAnim(RawFile):
    ext = ".BMA0"
    
class BasicVisibilityAnim(RawFile):
    ext = ".BVA0"
    
class BasicTexturePatternAnim(RawFile):
    ext = ".BTP0"
    
MagicLookup4 = {
    Magic.NITRO_COLOR_RES.value: ("Nitro Color Resource", NitroColorRes),
    Magic.NITRO_CHAR_GRAPHIC_RES.value: ("Nitro Char Graphics Resource", NitroCharGraphicRes),
    Magic.NITRO_SCREEN_RES.value: ("Nitro Screen Resource", NitroScreenRes),
    Magic.NITRO_FONT_RES.value: ("Nitro Font Resource", NitroFontRes),
    Magic.NITRO_ANIM_RES.value: ("Nitro Animation Resource", NitroAnimRes),
    Magic.NITRO_CELL_RES.value: ("Nitro Cell Resource", NitroCellRes),
    Magic.NITRO_MULT_ANIM_RES.value: ("Nitro Multi-Animation Resource", NitroModelAnimRes),
    Magic.NITRO_MULT_CELL_RES.value: ("Nitro Multi-Cell Resource", NitroModelCellRes),
    Magic.APS12_1.value: ("APS12_1 File", APS12_1),
    Magic.MAP_NG.value: ("Map Object Layout 'NG' file", MapNG),
    Magic.MAP_WB.value: ("Map Terrain 'WB' file", MapWB),
    Magic.MAP_RD.value: ("Map Terrain 'RD' file", MapRD),
    Magic.MAP_GC.value: ("Map Terrain 'GC' file", MapGC),
    Magic.BASIC_MODEL.value: ("Basic Model Data", BasicModel),
    Magic.BASIC_TEXTURE.value: ("Basic Texture Data", BasicTexture),
    Magic.BASIC_CHARA_ANIM.value: ("Basic Character Animation", BasicCharAnim),
    Magic.BASIC_TEXTURE_ANIM.value: ("Basic Texture Animation", BasicTextureAnim),
    Magic.BASIC_MAT_ANIM.value: ("Basic Material Animation", BasicMaterialAnim),
    Magic.BASIC_VIS_ANIM.value: ("Basic Visibility Animation", BasicVisibilityAnim),
    Magic.BASIC_TEXTURE_PAT_ANIM.value: ("Basic Texture Pattern Animation", BasicTexturePatternAnim)
}
    
class UnkFile01(RawFile):
    ext = ".unk01"    
    
MagicLookup2 = {
    #Magic.FILE_01.value: ("Unknown '01' format", UnkFile01)
}
    
def Magic_ID(byt):     
    
    if len(byt) == 0:
        return "Empty", None
    
    try:
        pair = MagicLookup4[byt]
    except:
        try:
            pair = MagicLookup2[byt[:2]]
        except:
            return f"Raw Data {bytes(byt)}", RawFile
    
    return pair[0], pair[1]

