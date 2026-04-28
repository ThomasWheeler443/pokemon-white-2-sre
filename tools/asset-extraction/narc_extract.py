# narc_extract.py
# thomwheeler04@vt.edu - thomaswheeler443@gmail.com
#
# Extract proprietary 'Nitro Archive (NARC)' files
# Into the base contents

from asset_tools.narc import Narc
from asset_tools.narcless import Narcless
import sys

def main():
    if sys.argv[1].endswith("utility.bin"):
        narc = Narcless(sys.argv[1], sys.argv[2])
    else:
        narc = Narc(sys.argv[1], sys.argv[2])
    narc.print()
    narc.extract()
    narc.close()

if __name__ == "__main__":
    main()
