# raw.py
# thomwheeler04@vt.edu - thomaswheeler443@gmail.com
#
# Initialize a raw file

from asset_tools.file_abc import FileFormatABC

class RawFile(FileFormatABC):
    
    ext = ""
    
    def create(self, data, name):
        self.data = data
        self.name = name
        
    def read(self, file_name):
        self.name = file_name
        with open(file_name, 'rb') as f:
            self.data = f.read() 
    
    def print(self):
        counter = 0
        for byte in self.data:
            
            print(f"{byte}", end=" ")
            counter += 1
            
            if counter >= 16:
                print()
                counter = 0
    
    def extract(self):
        if len(self.data) == 0:
            return
        with open(self.name, "wb") as f:
            f.write(self.data)
        