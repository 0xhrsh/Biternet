import os
from random import randint

class FileDistributor:
    def __init__(self, file_ID):
        self.fileID = "files\\" + file_ID
        self.valid = False
        self.sessionID = None
        self.filePointer = None
        
        if os.path.exists(self.fileID):
            self.valid = True
    
    def create_session(self):
        self.sessionID = randint(1000, 9999)
        self.filePointer = open(self.fileID)
        return self.sessionID

    def get_next_chunk(self, chunk_size=16):
        return self.filePointer.read(chunk_size)
