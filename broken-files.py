import os, sys, math, traceback, io

if sys.version_info[0] < 3:
    sys.exit('this script suppoorts only python v.3, sorry about that')

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from pathlib import Path


print('starting broken files search...')
for filename in Path('./').glob('**/*.png'):

    try:
        img = Image.open(filename)
        try: 
            img.getpixel((0,0))
        finally:
            img.close()

        img.close() 
    except Exception as e:
        print(filename, str(e))