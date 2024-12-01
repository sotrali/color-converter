# import sys
import argparse

# Order of types must match order of arguments defined
# (or else arg validation will no longer work properly)
TYPES = ['hex', 'rgb', 'cmyk']
# look into CMY, HSL, HSV

HEX_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']

def main():

    # Set up arguments
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-hex', action='store_true', help='convert from hex (accepts hexadecimal input [ffffff] or string ["#ffffff"] (both are case insensitive)')
    parser.add_argument('-rgb', action='store_true', help='convert from RGB (accepts integer input [R G B], or string [\"rgb(R, G, B)\"] (case/whitespace insensitive)')
    parser.add_argument('-cmyk', action='store_true', help='convert from CMYK (accepts integer input [C M Y K], or string [\"cmyk(C, M, Y, K)\"] (case/whitespace insensitive)')
    
    parser.add_argument('color', nargs='*', help='accepts a color in Hex, RGB, CMYK, or HSL and performs format conversions (does not support CMYK profiles, conversions are uncalibrated)')
    args = parser.parse_args()


    # debug print
    print(args)


    # INPUT SYNTAX VALIDATION
    if not validateArguments(args) :
        return;

    color = args.color
    
    # HANDLE HEX INPUT
    if args.hex :
        color = color[0].lower().replace(' ', '').strip('#')
        if not validateHex(color) :
            return

        convertFromHex(color)

    # HANDLE RGB INPUT
    if args.rgb :

        convertFromRGB(color)

    # HANDLE CMYK INPUT
    if args.cmyk :
        convertFromCMYK(color)




##
# HEX CONVERSION SECTION
##

# Takes in valid RGB code and converts it to the other formats
def convertFromHex(hexCode) :
    print('convert hex: ', hexCode, '\n')
    
    rgbValues = hexToRGB(hexCode)
    print("RGB: ", rgbValues)

    cmykValues = rgbToCMYK(rgbValues)
    print("CMYK: ", cmykValues)
    
    # convertToHSL('hex', code)

def rgbToHex(rgbValues) :
    hexValue = ''
    
    for rgbValue in rgbValues :
        hexValue += hex(int(rgbValue / 16)) 
        hexValue += hex(int(rgbValue % 16))
    
    return hexValue



 ##
# RGB CONVERSION SECTION
##

# Takes in valid RGB code and converts it to the other formats
def convertFromRGB(color) :
    # cleanse any non-numerical stuff
    if len(color) == 1 :
        color = color[0].lower().strip('rgb(').strip(')').replace(' ', '').split(',')
        
    rgbValues = validateRGB(color)
    if rgbValues is None :
        return
        
    for i in range(len(rgbValues)) :
        rgbValues[i] = int(rgbValues[i])

    print('convert RGB: ', rgbValues, '\n')
    
    hexCode = rgbToHex(rgbValues)
    print('Hex: ', hexCode)

    cmykValues = rgbToCMYK(rgbValues)
    print('CMYK: ', cmykValues)

    # convertToHSL('rgb', rgbValues)

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

def cmykToRGB(cmykValues) :
    x       = 1 - (cmykValues[3] / 100)
    red     = 255 * (1 - (cmykValues[0] / 100)) * x
    green   = 255 * (1 - (cmykValues[1] / 100)) * x
    blue    = 255 * (1 - (cmykValues[2] / 100)) * x
    
    return [int(red), int(green), int(blue)]




##
# CMYK CONVERSION SECTION
##

def convertFromCMYK(color) :
    # cleanse any non-numerical stuff
    if len(color) == 1 :
        color = color[0].lower().strip('cmyk(').strip(')').replace('%', '').replace(' ', '').split(',')

    cmykValues = validateCMYK(color) 
    if cmykValues is None :
        return

    print('convert CMYK: ', cmykValues, '\n')

    rgbValues = cmykToRGB(cmykValues)
    print('RGB: ', rgbValues)

    hexCode = rgbToHex(rgbValues)
    print('Hex: ', hexCode)

def rgbToCMYK(rgbValues) :
    # Normalize RGB values
    normalRed   = rgbValues[0] / 255
    normalGreen = rgbValues[1] / 255
    normalBlue  = rgbValues[2] / 255

    # Establish black
    black       = 1 - max(normalRed, normalGreen, normalBlue)
    x           = 1 - black
    
    # Convert
    cyan        = (1 - normalRed - black)   / x
    magenta     = (1 - normalGreen - black) / x
    yellow      = (1 - normalBlue - black)  / x
    
    return [round(cyan * 100, 2), round(magenta * 100, 2), round(yellow * 100, 2), round(black * 100, 2)]



##
# INPUT VALIDATION SECTION
##

# Takes in a string. Returns True if valid Hex color code.
def validateHex(value) :
    if len(value) != 6 :
        print('ERROR: Improper number of values for hex (should be 6 digits)')
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
def validateCMYK(values) :
    intValues = []

    if len(values) != 4 :
        print('ERROR: Improper number of values for CMYK (should be 4)')
        return
    
    for value in values :
        if not value.isnumeric() :
            print('ERROR: Improper format for CMYK value(s). All values must be numeric and between 0-100(%)!')
            return
        value = int(value)
        intValues.append(value)
        if (value < 0) or (value > 100) :
            print('ERROR: Each CMYK value must be between 0-100(%)')
            return
    
    return intValues

# Takes in the program's arguments generated by argparse. Returns True if valid arguments
def validateArguments(args) :
    # First, check that only one input flag is being used
    flagsActive = 0
    for flag in range(len(vars(args))-1) :
        # this uses our TYPES list to key into the args dictionary and determine how many flags are True
        if vars(args)[TYPES[flag]] :
            flagsActive += 1
        if flagsActive > 1 :
            print('ERROR: Currently this tool only supports one input type at a time. Too many flags!')
            return False

    # Second, check that there is a color code to convert
    if len(args.color) == 0 :
        print('ERROR: Must enter both an input flag and color code (did you forget to wrap color code in quotes?)\nFor more info, use the \'-h\' or \'--help\' flag.')
        return False
    
    return True





##
# GENERAL UTILITIES
##

# Takes in a decimal number and converts it to hexadecimal
def hex(number) :
    number = int(number)
    if number > 16 :
        print("ERROR: Decimal to Hexidecimal conversion failed")
        return "ERROR: Decimal to Hexidecimal conversion failed" 
    if number < 10 :
        return str(number)
    return HEX_LETTERS[number % 10]



if __name__ == '__main__' :
    main()
