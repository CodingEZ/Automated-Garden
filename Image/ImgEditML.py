import os
from PIL import Image


def rename_dir(directory):
    files = os.listdir(directory)
    index = 0
    for name in files:
        extension = '.' + name.split('.')[1]
        src = os.path.join(directory, name)
        while os.path.exists(os.path.join(directory, str(index) + extension)):
            index += 1
        dst = os.path.join(directory, str(index) + extension)
        os.rename(src, dst)
        index += 1

def resize_dir(directory, width, height):
    newFolder = directory + '_small'
    if not os.path.exists(newFolder):
        os.mkdir(newFolder)
    for file in os.listdir(directory):
        img = Image.open(os.path.join(directory, file))
        img = img.resize((width, height), Image.ANTIALIAS)  # image resize filter
        dst = os.path.join(newFolder, file)
        if os.path.exists(dst):
            os.remove(dst)
        try:
            img.save(dst, 'JPEG')
        except:
            # presence of alpha channel
            convertImg = Image.new("RGB", img.size, (255, 255, 255))
            convertImg.paste(img, mask=img.split()[3]) # 3 is the alpha channel
            convertImg.save(dst, 'JPEG')

def remove_files(directory, width, height):
    for file in os.listdir(directory):
        img = Image.open(os.path.join(directory, file))
        if img.size[0] < width or img.size[1] < height:
            print(img.size)
            print(file)

def remove_duplicates(directory):
    import cv2
    import numpy as np

    imgs = []
    for file in os.listdir(directory):
        img = cv2.imread(os.path.join(directory, file))

        result = False
        for image in imgs:
            try:
                difference = cv2.subtract(img, image)
                result = not np.any(difference)
                if result is True:
                    os.remove(os.path.join(directory, file))
                    print(file)
                    break
            except:
                continue
        if result is False:
            imgs.append(img)

#rename_dir('Weed-Broadleaf_Plantain')
#rename_dir("Plant-Lettuce")
#resize_dir('Weed-Broadleaf_Plantain', 100, 100)
