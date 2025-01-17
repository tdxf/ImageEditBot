import html
import random
import numpy as np
import numexpr as ne
import math
from multiprocessing import Pool
import urllib.request

from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageOps, ImageEnhance

from impact import make_caption


value_global = ""


#####################################
# HELPER FUNCTIONS FOR THE COMMANDS #
#####################################


def args_to_array(value, min_args):
    """
    Converts a string of arguments seperated by ";" to a list of values
    """
    value = value.split(';')

    if len(value) < min_args:
        raise Exception("not enough arguments")

    return value


def convert_all_to_int(array):
    """
    Used to convert an array of string args to ints
    """
    
    for i in array:
        array[i] = int(array[i].strip())

    return array


#####################
# COMMAND FUNCTIONS #
#####################


def crop(value, img):
    """
    Crops image by percent

    args:
    x;y;width;height
    """

    # Convert the argument string to a list of ints
    values = convert_all_to_int(args_to_array(value, 4))

    # Limit the values to 0-100 so they're percentages
    # Then divide the values by 100 so multiplying a number
    # with them yields the <value> percentile of that number
    # Also deconstruct the list into variables
    x, y, w, h = map(lambda x: np.clip(int(x), 0, 100) / 100, values)
    
    
    # Crop the image, by percentages
    return img.crop((x * img.size[0], 
                     y * img.size[1], 
                     w * img.size[0], 
                     h * img.size[1]))


def blur(value, img):
    try:
        value = np.clip(int(value), 0, 100)
    except:
        raise Exception("Error with blur value")
    
    return img.filter(ImageFilter.GaussianBlur(value))


def flip(value, img):
    """
    args:
    h or v
    """
    
    if value == "h":
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    elif value == "v":
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        raise Exception("Argument error for flip")
        return
        

def impact(value, img):
    """
    args:
    toptext;bottomtext
    """

    values = args_to_array(value, 1)

    top_text = values[0]
    bottom_text = values[1] if len(values) != 1 else None

    make_caption(img, top_text, bottom_text)

    return img


# TODO automate min max and median
def minfunc(value, img):
    """Applies the min filter to 'img'"""
    try:
        value = np.clip(int(value), 0, 17)
    except:
        raise Exception("Argument error for min")

    return img.filter(ImageFilter.MinFilter(value))


def maxfunc(value, img):
    #value = number
    
    try:
        value = int(value)
    except:
        raise Exception("there is something wrong with max value")
    
    return img.filter(ImageFilter.MaxFilter(value))
    

def median(value, img):
    #value = number
    
    try:
        value = int(value)
    except:
        raise Exception("there is something wrong with median value")
    
    return img.filter(ImageFilter.MedianFilter(value))
    

def contrast(value, img):
    try:
        value = edit_functions.clamp(int(value), -1000, 1000)
    except:
        raise Exception("Argument error for contrast")

    value = (259 * (value + 255)) / (255 * (259 - value))

    def c(x):
        x = 128 + value * (x - 128)
        return max(0, min(255, x))

    return img.point(c)


#def repeat(value, img):
#    #value = number;number
#    
#    value = args_to_array(value, 2)
#    
#    self.img = self.img.resize((self.img.width // value[0], self.img.height // value[1]))
#    self.img = edit_functions.get_concat_tile_repeat(self.img, value[0], value[1])

    
#def resize(self, value):
#    #value = number;number
#    
#    value = args_to_array(value, 2)
#    
#    self.img = self.img.resize((edit_functions.clamp(value[0], 1, 8192), edit_functions.clamp(value[1], 1, 8192)))
    

#def brightness(self, value):
#    try:
#        value = int(value)
#    except:
#        raise Exception("there is something wrong with brightness value")
#    
#    applier = ImageEnhance.Brightness(self.img)
#    
#    self.img = applier.enhance(value)
    

#def hue(self, value):
#    #value = number
#    try:
#        value = int(value)
#    except:
#        raise Exception("there is something wrong with hue value")
#    
#    HSV = self.img.convert("HSV")
#    H, S, V = HSV.split()
#    H = H.point(lambda x : value)
#    self.img = PillImage.merge("HSV", (H, S, V)).convert("RGB")


#def wave(self, value):
#    #value = number;number
#    value = args_to_array(value, 2)
#    
#    A = self.img.width / value[1]
#    w = value[0] / self.img.height
#    shift = lambda x: A * numpy.sin(2.0 * numpy.pi * x * w)
#    
#    arr = numpy.array(self.img)
#    
#    for i in range(self.img.width):
#        arr[:, i] = numpy.roll(arr[:, i], int(shift(i)))
#        
#        self.img = PillImage.fromarray(arr)


#def glitch(self, value):
#    #value = true or false
#    if not value == "true":
#        try:
#            value = edit_functions.clamp(int(value), -256, 256)
#        except:
#            raise Exception("there is something wrong with glitch value")
#        
#        arr = numpy.array(self.img)
#        
#            for i in range(self.img.width):
#                arr[:, i] = numpy.roll(arr[:, i], random.randrange(-value, value))
#                
#                self.img = PillImage.fromarray(arr)
#            else:
#                self.img = self.img.point(lambda x : random.randint(-256, 256))


#def square_crop(self, value):
#        # value = number
#        value = int(value)
#
#        half_size_x = self.img.size[0] // 2
#        half_size_y = self.img.size[1] // 2
#
#        self.img = self.img.crop((  half_size_x - value,
#                                    half_size_y - value,
#                                    half_size_x + value,
#                                    half_size_y + value))
    

#def binary(self, value):
#        self.grayscale("true")
#        value = int(value)
#        pixels = self.img.load()
#        
#        for i in range(self.img.size[0]):
#                for j in range(self.img.size[1]):
#                    if pixels[i, j] >= value:
#                        pixels[i, j] = 255
#                    else:
#                        pixels[i, j] = 0


#def light(self,value):
#        value = float(value)
#
#        max_radius = self.img.width if self.img.width < self.img.height else self.img.height
#        img = self.img.load()
#        center = (self.img.width // 2, self.img.height // 2)
#
#        max_x = abs(max_radius - center[0])
#        max_y = abs(max_radius - center[1])
#
#
#        max_distance = math.sqrt(max_x * max_x + max_y * max_y)
#
#        for i in range(self.img.width):
#            for j in range(self.img.height):
#
#                x = abs(i - center[0])
#                y = abs(j - center[1])
#
#                distance = math.sqrt(x * x + y * y)
#                img[i ,j] = tuple(map(lambda x : int(x * (1 - (distance / max_distance * value)) * 3), img[i ,j]))


##########################################
# HELPER FUNCTIONS FOR THE COMMANDS LIST #
##########################################


def lambda_filter(imgfilter):
    """
    Returns a lambda with two arguments
    if the first argument is the string "true", 'imgfilter' is applied to the second argument
    """

    return lambda value, img : img.filter(imgfilter) if value == "true" else img
    
def lambda_function(func):
    """
    Returns a lambda with two arguments
    if the first argument is the string "true", 'func' is applied to the second argument
    """

    return lambda value, img : func(img) if value == "true" else img


def lambda_function_adv(func, minval, maxval):
    """
    Returns a function with two arguments

    the first argument is a string
    that string is converted to an int and clamped between 'minval' and 'maxval'

    The second argument is an image
    """
    def fun(value, img):
        try:
            value = np.clip(int(value), minval, maxval)
        except:
            raise Exception("Argument error")
        
        return func(img, value)

    return fun
        
                
#################
# COMMANDS LIST #
#################

commands_list = {
    "rotate": lambda value, img : img.rotate(value, expand=True),

    "contour": lambda_filter(ImageFilter.CONTOUR),
    "enhance": lambda_filter(ImageFilter.EDGE_ENHANCE_MORE),
    "emboss": lambda_filter(ImageFilter.EMBOSS),
    "edges": lambda_filter(ImageFilter.FIND_EDGES),

    "grayscale": lambda_function(ImageOps.grayscale),
    "invert": lambda_function(ImageOps.invert),

    "crop": crop,
    "blur": blur,
    "flip": flip,
    "impact": impact,
    "min": minfunc,
    "max": maxfunc,
    "median": median,
    "contrast": contrast,

    "solarize": lambda_function_adv(ImageOps.solarize, -100, 100)
    }
