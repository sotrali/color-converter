import math
import argparse

# Order of types must match order of arguments defined
# (or else arg validation will no longer work properly)
TYPES = ['hex', 'rgb', 'cmy', 'cmyk']
# look into CMY, HSL, HSV

HEX_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']

def main():

    # Set up arguments
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-hex', action='store_true', help='convert from hex (accepts hexadecimal input [ffffff] or string ["#ffffff"] (case insensitive, "#" is optional in string)')
    parser.add_argument('-rgb', action='store_true', help='convert from RGB (accepts integer input [R G B], or string [\"rgb(R, G, B)\"] (case/whitespace insensitive)')
    parser.add_argument('-cmy', action='store_true', help='convert from CMY (accepts integer input [C M Y], or string [\"cmy(C, M, Y)\"] (case/whitespace insensitive)')
    parser.add_argument('-cmyk', action='store_true', help='convert from CMYK (accepts integer input [C M Y K], or string [\"cmyk(C, M, Y, K)\"] (case/whitespace insensitive)')
    parser.add_argument('color', nargs='*', help='accepts a color in Hex, RGB, CMY, CMYK, or HSL and performs format conversions (does not support CMYK profiles, conversions are uncalibrated)')
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




##
# COLOR HANDLERS
##

# Takes in valid RGB code and converts it to the other formats
def handleHex(color) :
    # cleanse hex code
    hexCode = color[0].lower().replace(' ', '').strip('#')
    if not validateHex(hexCode) :
        return

    print('convert hex: ', hexCode, '\n')

    rgbValues = hexToRGB(hexCode)
    cmyValues = rgbToCMY(rgbValues)
    cmykValues = rgbToCMYK(rgbValues)

    print("RGB: ", rgbValues)
    print("CMY: ", cmyValues)
    print("CMYK: ", cmykValues)

   # convertToHSL('hex', code)

# Takes in valid RGB code and converts it to the other formats
def handleRGB(color) :
    # cleanse any non-numerical stuff
    if len(color) == 1 :
        color = color[0].lower().strip('rgb(').strip(')').replace(' ', '').split(',')
        
    rgbValues = validateRGB(color)
    if rgbValues is None :
        return
        
    # for i in range(len(rgbValues)) :
        # rgbValues[i] = int(rgbValues[i])

    print('convert RGB: ', rgbValues, '\n')
    
    hexCode = rgbToHex(rgbValues)
    cmyValues = rgbToCMY(rgbValues)
    cmykValues = rgbToCMYK(rgbValues)
    
    print('CMYK: ', cmykValues)
    print('Hex: ', hexCode)
    print('CMY: ', cmyValues)

    # convertToHSL('rgb', rgbValues)

def handleCMY(color) :
    # cleanse any non-numerical stuff
    if len(color) == 1 :
        color = color[0].lower().strip('cmy(').strip(')').replace('%', '').replace(' ', '').split(',')
    cmyValues = validateCMYK(color, False) 
    if cmyValues is None :
        return

    print('convert CMY: ', cmyValues, '\n')

    rgbValues = cmyToRGB(cmyValues)
    hexCode = rgbToHex(rgbValues)
    cmykValues = rgbToCMYK(rgbValues)

    print('Hex: ', hexCode)
    print('RGB: ', rgbValues)
    print('CMYK: ', cmykValues)

def handleCMYK(color) :
    # cleanse any non-numerical stuff
    if len(color) == 1 :
        color = color[0].lower().strip('cmyk(').strip(')').replace('%', '').replace(' ', '').split(',')
    cmykValues = validateCMYK(color, True) 
    if cmykValues is None :
        return

    print('convert CMYK: ', cmykValues, '\n')

    rgbValues = cmykToRGB(cmykValues)
    hexCode = rgbToHex(rgbValues)
    cmyValues = rgbToCMY(rgbValues)

    print('Hex: ', hexCode)
    print('RGB: ', rgbValues)
    print('CMY: ', cmyValues)





##
#  CONVERSION SECTION
##

# Takes in a string, returns a list of 3 integers
def hexToRGB(hexCode) :
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
def rgbToHex(rgbValues) :
    hexValue = ''

    for rgbValue in rgbValues :
        hexValue += hex(rgbValue / 16) 
        hexValue += hex(rgbValue % 16)
    
    return hexValue

# Takes in a list of 3 integers, returns a list of 3 floats (percentages)
def rgbToCMY(rgbValues) :
    # Normalize RGB values
    normalRed   = rgbValues[0] / 255
    normalGreen = rgbValues[1] / 255
    normalBlue  = rgbValues[2] / 255

    # Convert
    cyan    = 1 - normalRed 
    magenta = 1 - normalGreen
    yellow  = 1 - normalBlue 

    return [round(cyan * 100, 2), round(magenta * 100, 2), round(yellow * 100, 2)]

# Takes in a list of 3 integers, returns a list of 4 floats (percentages)
def rgbToCMYK(rgbValues) :
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
    
    return [round(cyan * 100, 2), round(magenta * 100, 2), round(yellow * 100, 2), round(black * 100, 2)]

# Takes in a list of 3 floats, returns a list of 3 integers
def cmyToRGB(cmyValues) :
    red     = (1 - (cmyValues[0] / 100)) * 255
    green   = (1 - (cmyValues[1] / 100)) * 255
    blue    = (1 - (cmyValues[2] / 100)) * 255
    
    return [smartRound(red), smartRound(green), smartRound(blue)]

# Takes in a list of 4 floats, returns a list of 3 integers
def cmykToRGB(cmykValues) :
    x       = 1 - (cmykValues[3] / 100)
    red     = 255 * (1 - (cmykValues[0] / 100)) * x
    green   = 255 * (1 - (cmykValues[1] / 100)) * x
    blue    = 255 * (1 - (cmykValues[2] / 100)) * x
    
    return [smartRound(red), smartRound(green), smartRound(blue)]


##
# VALIDATION SECTION
##

# Takes in a string. Returns True if valid Hex color code.
def validateHex(value) :

    if len(value) != 6 :
        print('ERROR: Improper format for hex code (see --help)')
        return False

    for i in range(len(value)):
        if value[i-1].isnumeric() :
            continue
        elif HEX_LETTERS.count(value[i-1]) != 0 :
            continue
        else :
            print('ERROR: Invalid character in hex code')
            return False

    return True

# Takes in a list of strings. Returns same list as integers if valid RGB values. 
def validateRGB(values) :
    intValues = []

    if len(values) != 3 :
        print('ERROR: Improper number of values for RGB (should be 3)')
        return 

    for value in values :
        if not value.strip().isnumeric() :
            print('ERROR: Improper format for RGB value(s)')
            return 
        value = int(value)
        intValues.append(value)
        if (value < 0) or (value > 255) :
            print('ERROR: Each RBG value must be between 0-255')
            return 
    
    return intValues

# Takes in a list of strings. Returns same list as integers if valid CMYK values.
def validateCMYK(values, include_K) :
    floatValues = []

    if (include_K and len(values) != 4) :
        print('ERROR: Improper number of values for CMYK (should be 4)')
        return

    if (not include_K and len(values) != 3) :
        print('ERROR: Improper number of values for CMY (should be 3)')
        return

    for value in values :
        if not value.replace('.', '').isnumeric() :
            print('ERROR: Improper format for CMY(K) value(s). All values must be numeric and between 0.0-100.0(%)!')
            return
        value = float(value)
        floatValues.append(value)
        if (value < 0) or (value > 100) :
            print('ERROR: Each CMY(K) value must be between 0,0-100.0(%)')
            return
    
    return floatValues

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
