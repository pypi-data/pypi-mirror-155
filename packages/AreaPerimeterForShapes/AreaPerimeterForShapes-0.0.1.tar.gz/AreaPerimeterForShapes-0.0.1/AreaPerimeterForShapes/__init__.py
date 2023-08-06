import math


def rectangleArea(length, breadth):
    return length * breadth


def rectanglePerimeter(length, breadth):
    return 2*(length + breadth)


def circleArea(radius):
    return math.pi * math.pow(radius, 2)


def circlePerimeter(radius):
    return 2 * math.pi * radius


def trianglePerimeter(**kwargs):
    if 'side' in kwargs.keys():
        return kwargs['side']
    else:
        return kwargs['base'] + (2*(kwargs['height'] * 2 / math.sqrt(3)))


def traingleArea(**kwargs):
    if 'side' in kwargs.keys():
        return (math.sqrt(3) / 4) * math.pow(kwargs['side'], 2)
    else:
        return (1/2) * kwargs['base'] * kwargs['height']


print(traingleArea(side=5))
