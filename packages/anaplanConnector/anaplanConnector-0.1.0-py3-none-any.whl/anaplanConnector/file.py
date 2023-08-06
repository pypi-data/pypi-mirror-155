import os
from math import ceil

class File:
    def __init__(self, chunkSize=50):
        """
        :filepath is the relative path or full path to the loaded file e.g. ./load.csv or /home/user/file.txt
        :chunksize is the size of each chunk in MB. Default is 50MB.
        """
        self.chunkSizeBytes = chunkSize * 1024 * 1024
    
    def setFilepath(self, filepath):
        self._filepath = filepath
        self.filesize = os.path.getsize(self._filepath)
        self.chunkCount = ceil(self.filesize / self.chunkSizeBytes)

    def getFileData(self):
        return open(self._filepath,'rb')

    def fileChunks(self):
        file = open(self._filepath,'rb')
        while True:
            data = file.read(self.chunkSizeBytes)
            if not data:
                break
            yield data