import os, datetime, csv, sys
from py_essentials import hashing as hs
from progress.bar import ShadyBar as Bar
from .utils import crc32, convert_size, fileCount

class FileListGenerator:
    base_path = os.path.dirname(sys.modules['__main__'].__file__)
    def __init__(self, folder = base_path):
        self.scan_dir = folder
        self.output_path = 'output/'
        self.output_file_name = ''
        self.filter_extensions = None

    def write_to_csv(self, filename, path='output/'):
        self.output_file_name = filename
        self.output_path = path
        file_path = self.output_path + self.output_file_name

        # IF OUTPUT FOLDER NOT CREATED
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        # IF CSV FILE NOT CREATED
        if not os.path.isfile(file_path):            
            with open(file_path, 'w+') as f:
                f.close()

        self.f=open(file_path, 'r+', encoding='utf-8')
        self.w=csv.writer(self.f, lineterminator='\n')
        return self.w

    def generate(self, monitor=False, filename='exported_list.csv'):
        if monitor:
            self.bar = Bar('Processing (%(index)d/%(max)d)', max=fileCount(self.scan_dir, allowed_extensions=self.filter_extensions), suffix='%(percent).0f%%  [Remaining: %(eta)ds]' )

        csv = self.write_to_csv(filename=filename)

        for path, dirs, files in os.walk(self.scan_dir):
            if dirs == dirs:
                for file in files:              
                    if self.filter_extensions and not file.endswith(self.filter_extensions):
                        continue
                    file_path = os.path.join(path, file)

                    file_name = os.path.basename(file_path)
                    file_dir_path = path.replace(self.scan_dir, '')
                    
                    file_name, file_ext = os.path.splitext(file_name)
                    file_size = os.path.getsize(file_path)

                    file_created_time = os.path.getctime(file_path)
                    file_created_on = datetime.datetime.fromtimestamp(file_created_time)
                    file_modified_time = os.path.getmtime(path)
                    file_modified_on = datetime.datetime.fromtimestamp(file_modified_time)

                    file_hash_crc32 = crc32(file_path)
                    file_hash_sh1 = hs.fileChecksum(file_path, "sha1")
                    file_hash_md5 = hs.fileChecksum(file_path, "md5")
                    
                    csv.writerow([
                        file_name, 
                        file_ext,
                        convert_size(file_size), 
                        file_dir_path, 
                        file_created_on, 
                        file_modified_on, 
                        file_hash_crc32, 
                        file_hash_sh1, 
                        file_hash_md5
                    ])

                    if monitor:
                        self.bar.next()