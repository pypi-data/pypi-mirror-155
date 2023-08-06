## CSV Files List Generator from Folders with Subfolders

### Installaion

`pip install python-export-file-info`

**Import:**
```
from csv_filelist_generator import FileListGenerator
```

---
**Full Code Example:**
```
from python_export_file_info import FileListGenerator
scan_folder_path = r"C:\Users\sannjayy\Desktop"
folder = FileListGenerator(scan_folder_path)
folder.filter_extensions = ('.mp4', '.mp3')
folder.generate(monitor=True, filename='pyfiles.csv')
```

To Filter by Extensions: `folder.filter_extensions = ('.mp4', '.mp3')` must be a tuple or list.

---


**`Generate` Options:**

| Syntax | Default | Options | Description |
| ------- | ------- | ------------ |  ------------------ |
| **monitor** | *False* | True / False |Show Process Bar on Terminal
| **filename** | exported_list.csv | *any* | CSV Output Filename

Default Output Folder: **output/** *[In Project Root]*

---



