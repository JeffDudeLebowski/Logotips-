import os, sys, math, traceback, io

if sys.version_info[0] < 3:
    sys.exit('this script suppoorts only python v.3, sorry about that')

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from pathlib import Path


print('starting broken files search...')
for filename in Path('./').glob('**/*.png'):

    try:
        # img = Image.open(filename)
        img = Image.open("Football/International/Italy/Juventus.png")
        # img = Image.open("Football/International/Switzerland/FC La Chaux De Fonds_sq.png")
        try: 
            print('img mode', img.mode)
            if (img.mode == 'RGB'):
                raise Exception('image is not transparent')  
            if (img.mode == 'P'  and 'transparency' not in img.info):
                raise Exception('image is not transparent')  
            
            def hasColored(x,y): 
                pixelData = img.getpixel((x,y))
                if (img.mode == 'L' or img.mode == 'LA'):
                    return pixelData[1] > 0
                if (img.mode == 'RGBA'):   
                    return pixelData[3] > 0                 
                if (img.mode == 'P'):    
                    return pixelData != img.info['transparency']
                if (img.mode == 'CMYK'): 
                    print('CCCCCMYYYK', pixelData)
            width = img.size[0]
            height = img.size[1]

            cropTop = cropBottom = cropLeft = cropRight = -1

            def findTopBottom(): 
                top = bottom = -1
                for y in range(0, math.floor(height/2)):
                    for x in range(0, width):
                        if (hasColored(x,y) and top < 0):
                            top = y 
                        if (hasColored(x, height - y - 1) and bottom < 0):
                            bottom = height - y - 1
                        if (top >= 0 and bottom >= 0):
                            return [top, bottom]
                        
            def findLefRight(): 
                left = right = -1
                for x in range(0, math.floor(width/2)):
                    for y in range(0, height):
                        if (hasColored(x,y) and left < 0):
                            left = x 
                        if (hasColored(width - x - 1, y) and right < 0):
                            right = width - x - 1
                        if (left >= 0 and right >= 0):    
                            return [left, right]

            cropTop, cropBottom = findTopBottom()
            cropLeft, cropRight = findLefRight()
            print(cropTop, cropBottom, cropLeft, cropRight)

            img.getpixel((0,0))            
        finally:
            img.close()

        sys.exit()
        
    except Exception as e:
        print(filename, str(e))
        sys.exit()