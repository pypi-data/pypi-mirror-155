import os, math, zlib


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return f"{s} {size_name[i]}"


def crc32(fileName):
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X"%(prev & 0xFFFFFFFF)


def fileCount(folder, allowed_extensions=None):
    "count the number of files in a directory"
    count = 0
    for base, dirs, files in os.walk(folder):
        for file in files:
            if allowed_extensions and file.endswith(allowed_extensions) or not allowed_extensions:
                count += 1
    return count


