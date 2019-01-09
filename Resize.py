from PIL import Image

def get_extension_index(name):
    index = -1
    while name[index] != '.' and index > -len(name) + 1:
        index -= 1
    return index

def resize_image(name, windowSize, imgFormat='JPEG'):
    """Downsizes image to fit parameters. Unable to stretch small images."""
    img = Image.open(name)
    index = get_extension_index(name)
    extension = name[index:]

    if img.size[0] > windowSize[0]:
        width = windowSize[0]
    else:
        width = img.size[0]

    if img.size[1] > windowSize[1]:
        height = windowSize[1]
    else:
        height = img.size[1]

    img = img.resize((width, height), Image.ANTIALIAS)  # image resize filter
    img.save(name[:index] + 'COPY' + extension, imgFormat)

    return name[:index] + 'COPY' + extension
