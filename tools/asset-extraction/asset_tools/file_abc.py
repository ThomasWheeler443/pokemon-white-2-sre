from abc import ABC

class FileFormatABC(ABC):
    
    ext = ""
    
    def create(self, data, name):
        pass
    
    def read(self, file_name):
        pass
    
    def print(self):
        pass
    
    def extract(self):
        pass
