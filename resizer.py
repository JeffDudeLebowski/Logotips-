import os, sys, math, traceback
if sys.version_info[0] < 3:
    sys.exit('this script suppoorts only python v.3, sorry about that')

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from pathlib import Path

print('starting files processing...')
filesProcessed = 0
brokenFiles = []
for filename in Path('./').glob('**/*.png'):
    try:

        ##
        # renaming image if it has incorrect format
        filename = str(filename)
        newFilename = filename        
        if (filename[-5:].lower() == '..png'):      # image lib cannot open files named this way    
            newFilename =  filename.replace('..png', '.png')
            os.rename(filename, newFilename)
        if (filename[-5:].lower() == '_.png'):      # image lib cannot open files named this way
            newFilename =  filename.replace('_.png', '.png')
            os.rename(filename, newFilename)
        if (filename[-7:] == '_sq.png'): # logo filename should contain only club name and file extension
            newFilename =  filename.replace('_sq.png', '.png')
            os.rename(filename, newFilename)
        if (filename != newFilename):
            print("\n renamed", filename, newFilename)


        img = Image.open(newFilename)        
        try:             
            ##
            # cropping image so borders of the img will touch logo edges 
            def hasColored(x,y): 
                return img.getpixel((x,y))[3] > 0
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

            img = img.crop((cropLeft, cropTop, cropRight, cropBottom))
            
            ##
            # making it square
            w0 = img.size[0]
            h0 = img.size[1]

            if h0 > w0:
                h1 = h0
                w1 = h1
            else:
                w1 = w0
                h1 = w1
            x1 = -(w1 - w0)//2
            y1 = -(h1 - h0)//2

            img = img.transform((w1, h1), Image.EXTENT, (x1,y1,x1+w1,y1+h1))
            
            img.save(newFilename) 
        finally:
            img.close()
            
        sys.stdout.write("\r{0} files processed".format(filesProcessed))
        sys.stdout.flush()        
        filesProcessed += 1
    except Exception as e:
        # traceback.print_exception(e)
        # sys.exit()
        brokenFiles.append([newFilename, str(e)])

sys.stdout.flush()
print(filesProcessed, ' files were successfully processed.') 
if (len(brokenFiles) > 0): 
    print('failed to process following files: ('+str(len(brokenFiles))+')')
    for file, error in brokenFiles:
        print(file, error)

sys.exit('task complete, exiting')
