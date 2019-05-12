# Imports
import os

from PIL import Image

#=============================================================#
# Original image size is 2550 x 3300 pixels (Width x Height)  #
# New image size is about 1800 x 1200 pixels (Width x Height) #
#=============================================================#

def populateLists(startingPoint, width, height, y_coordinates = []):
    x = []
    y = []
    if y_coordinates == []:
        if startingPoint == 'right':
            for i in range(height):
                x.append(width - 1)
            for i in range(height):
                y.append(i)
            return x , y
        elif startingPoint == 'left':
            for i in range(height):
                x.append(0)
            for i in range(height):
                y.append(i)
            return x , y
    if y_coordinates != []:

        y_coordinates_distance = max(y_coordinates) - min(y_coordinates)

        if startingPoint == 'right':
            for i in range(y_coordinates_distance):
                x.append(width - 1)
            for i in range(y_coordinates_distance):
                y.append(i)
            return x , y
        elif startingPoint == 'left':
            for i in range(y_coordinates_distance):
                x.append(0)
            for i in range(y_coordinates_distance):
                y.append(i)
            return x , y

    if startingPoint == 'bottom':
        for i in range(width):
            x.append(i)
        for i in range(width):
            y.append(height - 1)
        return x , y
    elif startingPoint == 'top':
        for i in range(width):
            x.append(i)
        for i in range(width):
            y.append(0)
        return x , y

def findYCoordinates(imageFile):
    pix = imageFile.load()
    width = imageFile.size[0]
    height = imageFile.size[1]
    y_coordinates = []

    # Bottom to Top
    x, y = populateLists('bottom', width, height)
    for i in range(height):
        for ix in range(width):
            if pix[x[ix], y[ix]] == (255, 255, 255):
                y[ix] -= 1
            elif pix[x[ix], y[ix]] != (255, 255, 255):
                pass
    y_coordinates.append(max(set(y), key = y.count))

    # Top to Bottom
    x , y = populateLists('top', width, height)
    for i in range(height):
        for ix in range(width):
            if pix[x[ix], y[ix]] == (255, 255, 255):
                y[ix] += 1
            elif pix[x[ix], y[ix]] != (255, 255, 255):
                pass
    y_coordinates.append(max(set(y), key = y.count))

    return y_coordinates

def findXCoordinates(imageFile, y_coordinates):
    pix = imageFile.load()
    width = imageFile.size[0]
    height = imageFile.size[1]
    x_coordinates = []
    y_coordinates_distance = max(y_coordinates) - min(y_coordinates)

    # Right to left
    x, y = populateLists('right', width, height, y_coordinates)
    for i in range(width):
        for ix in range(y_coordinates_distance):
            if pix[x[ix], y[ix]] == (255, 255, 255):
                x[ix] -= 1
            elif pix[x[ix], y[ix]] != (255, 255, 255):
                pass
    x_coordinates.append(max(set(x), key = x.count))
    # Left to right
    x, y = populateLists('left', width, height, y_coordinates)
    for i in range(width):
        for ix in range(y_coordinates_distance):
            if pix[x[ix], y[ix]] == (255, 255, 255):
                x[ix] += 1
            elif pix[x[ix], y[ix]] != (255, 255, 255):
                pass
    x_coordinates.append(max(set(x), key = x.count))
    return x_coordinates

def returnBoxCoordinates(x, y):
    x_max = max(x)
    x_min = min(x)
    y_min = min(y)
    y_max = max(y)
    box = (x_min, y_min, x_max, y_max)
    return box

def main():
    # TODO: Add the ability to import from other folders.
    # TODO: Add error suppresion for TypeError from non string imageType
    for file in os.listdir('.'):
        if file.endswith(".JPG"):
            img = Image.open(file)
            fn, fext = os.path.splitext(file)

            print("Calculating y bounderies for image ...")
            y = findYCoordinates(img)
            print('Calculation complete. The y boundries are {} and {}'.format(y[0],y[1]))
            print("Calculating x bounderies for image ...")
            x = findXCoordinates(img, y)
            print('Calculation complete. The x boundries are {} and {}'.format(x[0],x[1]))
            box = returnBoxCoordinates(x,y)
            region = img.crop(box)
            print("Image Cropped.")
            region.save('imgs/{}.JPG'.format(fn))
            print("Image saved as img/{}.JPG.\nStarting Next Image...".format(fn))



if __name__ == '__main__':
    main()
