import datetime


file = open('./timelog.txt', 'a')       # 'a' appends to the end
...
tm = datetime.datetime.now().time()
txt = f'{tm.isoformat()}\n'
...
file.write(txt)
...

# close not needed if we code script that runs fast
# because python will automatically close all files
# flushing their contents before exit
file.close()


with open('./timelog.txt', 'a') as logfile:
    logfile.write('SMTH\n')

# now file is closed, FOR SURE



# now open file and read contents
import pathlib as pth
logfie = pth.Path('./timelog.txt')      # open accepts Path objects
with open(logfile, 'r') as log:
    first = log.read(10)          # first 10 symbols
    everything = log.read()       # read the rest as a whole, read is blocking
    print('Everything as a whole:', first + everything, sep='\n')
    # be careful when reading as whole
    # as files can take GiBs of size:
    # 1. takes time before we can get result
    # 2. it consumes memory
    # Solutions:
    # - for '\n' separated text, we can iterate through lines
    # - read in chunks - for binary, or text (if text not separated by newlines)

    where = log.tell()      # get current position
    log.seek(0)     # rewind file to the beginning
    # next operations will be from the beginning of the file

    for line in log:
        print(f'[len={len(line): <5}] {line!r}')
    

import random
# try writing some binary
with open('./binfile.bin', mode='wb') as f:
    sep = b'\x00' * 4
    rnd = random.randint(0, 1000)
    rnd = rnd.to_bytes(2, 'little')
    res = sep + rnd + sep
    f.write(res)
    

# try extracting image from archive
import zipfile
with zipfile.ZipFile('cat.zip') as fzip:
    name = 'cat.jpg'
    with fzip.open(name, 'r') as fin, open(name, 'wb') as fout:
        data = fin.read()
        fout.write(data)
    


# Before everything was ok, now what happens if there are some exceptions
##file = open('./other.txt', 'w')         # 'w' means file is always recreated
##
##file.write('My results:\n')
##l = list(range(100))
##ratio = max(l) / min(l)         # division by 0 here
##file.write(f'{ratio}')
##file.close()                    # this is never reached


# OLD style. How it was. Now we have context mgr
file = open('./other.txt', 'w', encoding='utf-8')

try:
    file.write('My results:\n')
    l = list(range(100))
    ratio = max(l) / min(l)         # division by 0 here
    file.write(f'{ratio}')
finally:
    file.close()


# Use context manager to ensure files are always closed
# no matter what exceptions were raised during their processing
with open('./other.txt', 'w') as file:
    file.write('My results:\n')
    l = list(range(100))
    ratio = max(l) / min(l)         # division by 0 here
    file.write(f'{ratio}')
