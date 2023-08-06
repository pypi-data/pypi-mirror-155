import os, datetime, csv
from py_essentials import hashing as hs
from progress.bar import ShadyBar as Bar
from .utils import crc32, convert_size, fileCount


class FileListGenerator:
     
    def __init__(self, folder):
        self.scan_dir = folder
        self.allowed_extensions = (".jpg",".mp4")
        self.bar = Bar('Processing (%(index)d/%(max)d)', max=fileCount(self.scan_dir, self.allowed_extensions), suffix='%(percent).0f%%  [Remaining: %(eta)ds]' )
        self.f=open("files.csv",'r+')
        self.w=csv.writer(self.f, lineterminator='\n')
    

    def generate(self):
        for path, dirs, files in os.walk(self.scan_dir):
            if dirs == dirs:
                for filename in files:

                    if not filename.endswith(self.allowed_extensions):
                        continue

                    file_path = os.path.join(path, filename)

                    file_name = os.path.basename(file_path)
                    
                    file_name, file_ext = os.path.splitext(file_name)
                    file_size = os.path.getsize(file_path)

                    file_created_time = os.path.getctime(file_path)
                    file_created_on = datetime.datetime.fromtimestamp(file_created_time)
                    file_modified_time = os.path.getmtime(path)
                    file_modified_on = datetime.datetime.fromtimestamp(file_modified_time)

                    file_hash_crc32 = crc32(file_path)
                    file_hash_sh1 = hs.fileChecksum(file_path, "sha1")
                    file_hash_md5 = hs.fileChecksum(file_path, "md5")

                    self.w.writerow([
                        file_name, 
                        file_ext,
                        convert_size(file_size), 
                        path.replace(self.scan_dir, ''), 
                        file_created_on, 
                        file_modified_on, 
                        file_hash_crc32, 
                        file_hash_sh1, 
                        file_hash_md5
                    ])

                    self.bar.next()