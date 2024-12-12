import math
import argparse

# Order of types must match order of arguments defined
# (or else arg validation will no longer work properly)
TYPES = ['hex', 'rgb', 'cmy', 'cmyk', 'hsl', 'hsv']
# look into LAB

HEX_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']

def main():

    # Set up arguments
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-hex', action='store_true', help='convert from hex (accepts hexadecimal input [ffffff] or string ["#ffffff"] (case insensitive, "#" is optional in string)')
    parser.add_argument('-rgb', action='store_true', help='convert from RGB (accepts integer input [R G B], or string [\"rgb(R, G, B)\"] (case/whitespace insensitive)')
    parser.add_argument('-cmy', action='store_true', help='convert from CMY (accepts integer input [C M Y], or string [\"cmy(C, M, Y)\"] (case/whitespace insensitive)')
    parser.add_argument('-cmyk', action='store_true', help='convert from CMYK (accepts integer input [C M Y K], or string [\"cmyk(C, M, Y, K)\"] (case/whitespace insensitive)')
    parser.add_argument('color', nargs='*', help='accepts a color in Hex, RGB, CMY, CMYK, or HSL and performs format conversions (does not support CMYK profiles, conversions are uncalibrated)')
    parser.add_argument('-hsl', action='store_true', help='convert from HSL (accepts integer input [H S L], or string [\"hsl(H, S, L)\"] (case/whitespace insensitive)')
    parser.add_argument('-hsv', action='store_true', help='convert from HSV (accepts integer input [H S V], or string [\"hsv(H, S, V)\"] (case/whitespace insensitive)')
    args = parser.parse_args()


    # debug print
    print(args)


    # INPUT SYNTAX VALIDATION
    if not validateArguments(args) :
        return;

    color = args.color
    
    # HANDLE HEX INPUT
    if args.hex :
        handleHex(color)

    # HANDLE RGB INPUT
    if args.rgb :
        handleRGB(color)
    
    if args.cmy :
        handleCMY(color)

    # HANDLE CMYK INPUT
    if args.cmyk :
        handleCMYK(color)
    
    # HANDLE HSL INPUT
    if args.hsl :
        handleHSVorHSL(color, 'hsl')

    # HANDLE HSV INPUT
    if args.hsv :
        handleHSVorHSL(color, 'hsv')



##
# COLOR HANDLERS
##

# Takes in valid RGB code and converts it to the other formats
def handleHex(color) :
    hexCode = validateHex(color)
    if hexCode is None :
        return

    print('convert hex: ', hexCode, '\n')

    rgbValues = HEXtoRGB(hexCode)
    cmyValues = RGBtoCMY(rgbValues)
    cmykValues = RGBtoCMYK(rgbValues)
    hslValues = RGBtoHSVorHSL(rgbValues, 'hsl')
    hsvValues = RGBtoHSVorHSL(rgbValues, 'hsv')

    print('RGB: ', rgbValues)
    print('CMY: ', cmyValues)
    print('CMYK: ', cmykValues)
    print('HSL: ', hslValues)
    print('HSV: ', hsvValues)


# Takes in valid RGB code and converts it to the other formats
def handleRGB(color) :
    rgbValues = validateRGB(color)
    if rgbValues is None :
        return
        
    print('convert RGB: ', rgbValues, '\n')
    
    hexCode = RGBtoHEX(rgbValues)
    cmyValues = RGBtoCMY(rgbValues)
    cmykValues = RGBtoCMYK(rgbValues)
    hslValues = RGBtoHSVorHSL(rgbValues, 'hsl')
    hsvValues = RGBtoHSVorHSL(rgbValues, 'hsv')
    
    print('CMYK: ', cmykValues)
    print('Hex: ', hexCode)
    print('CMY: ', cmyValues)
    print('HSL: ', hslValues)
    print('HSV: ', hsvValues)

def handleCMY(color) :
    cmyValues = validateCMYorCMYK(color, False) 
    if cmyValues is None :
        return

    print('convert CMY: ', cmyValues, '\n')

    rgbValues = CMYtoRGB(cmyValues)
    hexCode = RGBtoHEX(rgbValues)
    cmykValues = RGBtoCMYK(rgbValues)
    hslValues = RGBtoHSVorHSL(rgbValues, 'hsl')
    hsvValues = RGBtoHSVorHSL(rgbValues, 'hsv')

    print('Hex: ', hexCode)
    print('RGB: ', rgbValues)
    print('CMYK: ', cmykValues)
    print('HSL: ', hslValues)
    print('HSV: ', hsvValues)

def handleCMYK(color) :
    cmykValues = validateCMYorCMYK(color, True) 
    if cmykValues is None :
        return

    print('convert CMYK: ', cmykValues, '\n')

    rgbValues = CMYKtoRGB(cmykValues)
    hexCode = RGBtoHEX(rgbValues)
    cmyValues = RGBtoCMY(rgbValues)
    hslValues = RGBtoHSVorHSL(rgbValues, 'hsl')
    hsvValues = RGBtoHSVorHSL(rgbValues, 'hsv')

    print('Hex: ', hexCode)
    print('RGB: ', rgbValues)
    print('CMY: ', cmyValues)
    print('HSL: ', hslValues)
    print('HSV: ', hsvValues)

# isHSL determines whether the function should handle HSL or HSV
def handleHSVorHSL(color, handle) :
    validated = validateHSLorHSV(color, handle)
    if validated is None :
        return
    
    rgbValues = HSLorHSVToRGB(validated, handle)
    hexCode = RGBtoHEX(rgbValues)
    cmyValues = RGBtoCMY(rgbValues)
    cmykValues = RGBtoCMYK(rgbValues)
    if handle == 'hsl' :
        hsvValues = RGBtoHSVorHSL(rgbValues, 'hsv')   
    else : # is HSV
        hslValues = RGBtoHSVorHSL(rgbValues, 'hsl')

    print('Hex: ', hexCode)
    print('RGB: ', rgbValues)
    print('CMY: ', cmyValues)
    print('CMYK: ', cmykValues)
    if handle == 'hsl' :
        print('HSV: ', hsvValues)
    else :
        print('HSL: ', hslValues)




##
#  CONVERSION FUNCTIONS
##

# Takes in a string, returns a list of 3 integers
def HEXtoRGB(hexCode) :
    rgbValues = []

    tempSum = 0
    i = 0
    while i < 6 :
        tempSum += int(hexCode[i], 16) * 16
        tempSum += int(hexCode[i+1], 16)
        rgbValues.append(tempSum)
        i = i + 2
        tempSum = 0
    
    return rgbValues

# Takes in a list of 3 integers, returns a string
def RGBtoHEX(rgbValues) :
    hexValue = ''

    for rgbValue in rgbValues :
        hexValue += hex(rgbValue / 16) 
        hexValue += hex(rgbValue % 16)
    
    return hexValue

# Takes in a list of 3 integers, returns a list of 3 floats (percentages)
def RGBtoCMY(rgbValues) :
    # Normalize RGB values
    normalRed   = rgbValues[0] / 255
    normalGreen = rgbValues[1] / 255
    normalBlue  = rgbValues[2] / 255

    # Convert
    cyan    = 1 - normalRed 
    magenta = 1 - normalGreen
    yellow  = 1 - normalBlue 

    return [cyan * 100, magenta * 100, yellow * 100]

# Takes in a list of 3 integers, returns a list of 4 floats (percentages)
def RGBtoCMYK(rgbValues) :
    # Normalize RGB values
    normalRed   = rgbValues[0] / 255
    normalGreen = rgbValues[1] / 255
    normalBlue  = rgbValues[2] / 255

    black   = 1 - max(normalRed, normalGreen, normalBlue)
    x       = 1 - black
    
    # Convert
    if x == 0 :
        return [0, 0, 0, round(black * 100, 2)]    
    else :
        cyan    = (1 - normalRed - black)   / x
        magenta = (1 - normalGreen - black) / x
        yellow  = (1 - normalBlue - black)  / x
    
    return [cyan * 100, magenta * 100, yellow * 100, black * 100]

# Takes in a list of 3 integers, returns a list of 1 integer and 2 floats (percentages)
def RGBtoHSVorHSL(rgbValues, convertTo) :
    hue = 0
    saturation = 0.0
    value = 0.0
    lightness = 0.0

    # Normalize RGB values
    normalRed   = rgbValues[0] / 255
    normalGreen = rgbValues[1] / 255
    normalBlue  = rgbValues[2] / 255

    # Establish variables for formula
    xMax = max(normalRed, normalGreen, normalBlue)
    xMin = min(normalRed, normalGreen, normalBlue)
    chroma = xMax - xMin
    
    # Convert by following formula

    value = xMax
    lightness = (xMax + xMin) / 2

    if chroma == 0 :
        hue = 0
    elif value == normalRed :
        hue = 60 * (((normalGreen - normalBlue) / chroma) % 6 )
    elif value == normalGreen :
        hue = 60 * (((normalBlue - normalRed) / chroma) + 2)
    elif value == normalBlue :
        hue = 60 * (((normalRed - normalGreen) / chroma) + 4)

    if convertTo == 'hsl' :
        if (lightness != 0) and (lightness != 1) :
            saturation = (value - lightness) / min(lightness, 1 - lightness) 
        return [int(hue), saturation * 100, lightness * 100]
    else : # convert to HSV
        if value != 0 :
            saturation = chroma / value
        return [int(hue), saturation * 100, value * 100]


# Takes in a list of 3 floats, returns a list of 3 integers
def CMYtoRGB(cmyValues) :
    red     = (1 - (cmyValues[0] / 100)) * 255
    green   = (1 - (cmyValues[1] / 100)) * 255
    blue    = (1 - (cmyValues[2] / 100)) * 255
    
    return [smartRound(red), smartRound(green), smartRound(blue)]

# Takes in a list of 4 floats, returns a list of 3 integers
def CMYKtoRGB(cmykValues) :
    x       = 1 - (cmykValues[3] / 100)
    red     = 255 * (1 - (cmykValues[0] / 100)) * x
    green   = 255 * (1 - (cmykValues[1] / 100)) * x
    blue    = 255 * (1 - (cmykValues[2] / 100)) * x
    
    return [smartRound(red), smartRound(green), smartRound(blue)]

# Takes in a list with 1 integer and 2 floats (in that order), and returns 3 integers
def HSLorHSVToRGB(values, convertFrom) :
    normalSaturation = values[1] / 100
    normalLorV= values[2] / 100

    # Perform first part of conversion
    if convertFrom == 'hsl' :
        chroma = (1 - math.fabs((2 * normalLorV) - 1)) * normalSaturation
        m = normalLorV - (chroma / 2)
    else : # is HSV
        chroma = normalLorV * normalSaturation
        m = normalLorV - chroma
    
    hPrime = values[0] / 60
    temp = (hPrime % 2) - 1
    x = chroma * (1 - math.fabs(temp))
    
    if (hPrime >= 0) and (hPrime < 1) :
        R = chroma + m
        G = x + m
        B = 0 + m
        return [smartRound(R * 255), smartRound(G * 255), smartRound(B * 255)]
    elif (hPrime >= 1) and (hPrime < 2) :
        R = x + m
        G = chroma + m
        B = 0 + m
        return [smartRound(R * 255), smartRound(G * 255), smartRound(B * 255)]
    elif (hPrime >= 2) and (hPrime < 3) :
        R = 0 + m
        G = chroma + m
        B = x + m
        return [smartRound(R * 255), smartRound(G * 255), smartRound(B * 255)]
    elif (hPrime >= 3) and (hPrime < 4) :
        R = 0 + m
        G = x + m
        B = chroma + m
        return [smartRound(R * 255), smartRound(G * 255), smartRound(B * 255)]
    elif (hPrime >= 4) and (hPrime < 5) :
        R = x + m
        G = 0 + m
        B = chroma + m
        return [smartRound(R * 255), smartRound(G * 255), smartRound(B * 255)]
    elif (hPrime >= 5) and (hPrime <= 6) :
        R = chrome + m
        G = 0 + m
        B = x + m
        return [smartRound(R * 255), smartRound(G * 255), smartRound(B * 255)]
    else :
        print('RGB to HSV/HSL conversion failed')
        return

##
# INPUT VALIDATION 
##

# Takes in a string. Returns True if valid Hex color code.
def validateHex(value) :
    # cleanse hex code
    value = value[0].lower().replace(' ', '').strip('#')
 
    if len(value) != 6 :
        print('ERROR: Improper format for hex code (see --help)')
        return 

    for i in range(len(value)):
        if value[i-1].isnumeric() :
            continue
        elif HEX_LETTERS.count(value[i-1]) != 0 :
            continue
        else :
            print('ERROR: Invalid character in hex code')
            return 

    return value

# Takes in a list of 3 strings. Returns same list as integers if valid RGB values. 
def validateRGB(color) :
    # cleanse any non-numerical stuff if entered as string
    if len(color) == 1 :
        color = color[0].lower().strip('rgb(').strip(')').replace(' ', '').split(',')

    if len(color) != 3 :
        print('ERROR: Improper number of values for RGB (should be 3)')
        return 

    intValues = []
    for value in color :
        if not value.strip().isnumeric() :
            print('ERROR: Improper format for RGB value(s)')
            return 
        value = int(value)
        intValues.append(value)
        if (value < 0) or (value > 255) :
            print('ERROR: Each RBG value must be between 0-255')
            return 
    
    return intValues

# Takes in a list of 3 or 4 strings. Returns same list as integers if valid CMYK values.
def validateCMYorCMYK(color, include_K) :
    # cleanse any non-numerical stuf if entered as string
    if include_K and len(color) == 1 :
        color = color[0].lower().strip('cmyk(').strip(')').replace('%', '').replace(' ', '').split(',')
    elif not include_K and len(color) == 1 :
        color = color[0].lower().strip('cmy(').strip(')').replace('%', '').replace(' ', '').split(',')

    if (include_K and len(color) != 4) :
        print('ERROR: Improper number of values for CMYK (should be 4)')
        return
    elif (not include_K and len(color) != 3) :
        print('ERROR: Improper number of values for CMY (should be 3)')
        return

    floatValues = []
    for value in color :
        if not value.replace('.', '').isnumeric() :
            print('ERROR: Improper format for CMY(K) value(s). All values must be numeric and between 0.0-100.0(%)!')
            return
        value = float(value)
        floatValues.append(value)
        if (value < 0) or (value > 100) :
            print('ERROR: Each CMY(K) value must be between 0,0-100.0(%)')
            return
    
    return floatValues

# Takes in a list of 3 strings. Returns same list as 1 integer and 2 floats
def validateHSLorHSV(color, handle) :
    # cleanse color code if entered as string
    if len(color) == 1 :
        if handle == 'hsl' :
            color = color[0].lower().strip('hsl(').strip(')').replace('%', '').replace(' ', '').split(',')
        else : # is HSV
            color = color[0].lower().strip('hsv(').strip(')').replace('%', '').replace(' ', '').split(',')

    if len(color) != 3 :
        print('ERROR: Improper number of values for HSL/HSV (should be 3)')
        return

    for i in range(3) :
        if not color[i].replace('.', '').isnumeric() :
            print('ERROR: HSL/HSV values must be numeric')
            return
        if i == 0 :
            color[i] = smartRound(color[i])
        else :
            color[i] = float(color[i])

    if (color[0] < 0) or (color[0] > 255) :
        print('ERROR: Invalid hue value (should be 0-255)')
        return
    if (color[1] < 0) or (color[1] > 100) :
        print('ERROR: Invalid saturation value (should be 0.0-100.0)')
        return
    if (color[2] < 0) or (color[2] > 100) :
        print('ERROR: Invalid lightness/value value (should be 0.0-100.0)')
        return

    return [color[0], color[1], color[2]]

# Takes in the program's arguments generated by argparse. Returns True if valid arguments
def validateArguments(args) :
    # ck that only one input flag is being used
    flagsActive = 0
    for flag in range(len(vars(args))-1) :
        # this uses our TYPES list to key into the args dictionary and determine how many flags are True
        if vars(args)[TYPES[flag]] :
            flagsActive += 1
        if flagsActive > 1 :
            print('ERROR: Currently this tool only supports one input type at a time. Too many flags!')
            return False

    if (flagsActive == 0) or (len(args.color) == 0) :
        print('ERROR: Must enter both an input flag and color code (did you forget to wrap color code in quotes?)\nFor more info, use the \'-h\' or \'--help\' flag.')
        return False
    
    return True





##
# GENERAL UTILITIES
##

# Takes in a float, returns the nearest integer
def smartRound(value) :
    value = float(value)
    if (value % 1) > .50 :
        return math.ceil(value)
    else :
        return math.floor(value)

# Takes in a decimal number and converts it to hexadecimal
def hex(number) :
    number = int(number)
    if number > 16 :
        print("ERROR: Decimal to Hexidecimal conversion failed")
        return "ERROR: Decimal to Hexidecimal conversion failed" 
    if number < 10 :
        return str(number)
    return HEX_LETTERS[number % 10]

# init
if __name__ == '__main__' :
    main()
