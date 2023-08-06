import os, datetime, csv, sys
from py_essentials import hashing as hs
from progress.bar import ShadyBar as Bar
from .utils import crc32, convert_size, fileCount

class FileListGenerator:
    base_path = os.path.dirname(sys.modules['__main__'].__file__)
    def __init__(self, folder = base_path,  output_path='output/'):
        self.scan_dir = folder
        self.output_path = f'{output_path.strip("/")}/' 
        self.output_file_name = ''
        self.filter_extensions = None

    def write_to_csv(self, filename):
        self.output_file_name = filename if filename.endswith('.csv') else f'{filename}.csv'
        file_path = self.output_path + self.output_file_name

        # IF OUTPUT FOLDER NOT CREATED
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        # IF CSV FILE NOT CREATED
        if not os.path.isfile(file_path):            
            with open(file_path, 'w+') as f:             
                f.close()

        self.f=open(file_path, 'r+')
        self.w=csv.writer(self.f, lineterminator='\n')
        self.w.writerow(['id', 'name', 'ext', 'size', 'file', 'crc32', 'sha1', 'md5', 'updated_at', 'created_at'])
        return self.w

    def generate(self, filename='exported_list.csv', file_prefix=None, monitor=False, index=True):
        if monitor:
            self.bar = Bar('Processing (%(index)d/%(max)d)', max=fileCount(self.scan_dir, allowed_extensions=self.filter_extensions), suffix='%(percent).0f%%  [Remaining: %(eta)ds]' )

        csv = self.write_to_csv(filename=filename)
        count = 1
        for path, dirs, files in os.walk(self.scan_dir):
            if dirs == dirs:
                for file in files:              
                    if self.filter_extensions and not file.endswith(self.filter_extensions):
                        continue
                    file_path = os.path.join(path, file)
                    file_name = os.path.basename(file_path)

                    file_new_path = path.replace(self.scan_dir, '').replace('\\','/') + '/' + file_name
                    file_prefix = f'{file_prefix.strip("/")}/' if file_prefix else ''
                    file_new_path = file_prefix + file_new_path.lstrip("/")

                    file_name, file_ext = os.path.splitext(file_name)
                    file_size = os.path.getsize(file_path)

                    file_created_time = os.path.getctime(file_path)
                    file_created_on = datetime.datetime.fromtimestamp(file_created_time).strftime("%Y-%m-%d %H:%M:%S")
                    file_modified_time = os.path.getmtime(path)
                    file_modified_on =  datetime.datetime.fromtimestamp(file_modified_time).strftime("%Y-%m-%d %H:%M:%S")

                    file_hash_crc32 = crc32(file_path)
                    file_hash_sh1 = hs.fileChecksum(file_path, "sha1")
                    file_hash_md5 = hs.fileChecksum(file_path, "md5")

                    csv.writerow([
                        count if index else '',
                        file_name, 
                        file_ext,
                        convert_size(file_size), 
                        file_new_path, 
                        file_hash_crc32, 
                        file_hash_sh1, 
                        file_hash_md5,                        
                        file_modified_on, 
                        file_created_on
                    ])
                    count += 1
                    if monitor:
                        self.bar.next()