import math
import argparse

TYPES = ['hex', 'rgb', 'cmy', 'cmyk', 'hsl', 'hsv']
# look into LAB

HEX_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']

OUTPUT_DESTINATION  = 'stdout'
VERBOSE = False


def main():

    ''' ESTABLISH ARGS '''
    parser = argparse.ArgumentParser(prog='color-converter', description='Color code converting utility written in Python.', epilog='Hope this helps :)')
    
    parser.add_argument('-hex',  action='store_true', help='convert/output to Hex')
    parser.add_argument('-rgb',  action='store_true', help='convert/output to RGB')
    parser.add_argument('-cmy',  action='store_true', help='convert/output to CMY')
    parser.add_argument('-cmyk', action='store_true', help='convert/output to CMYK (CMYK conversions are uncalibrated)')
    parser.add_argument('-hsl',  action='store_true', help='convert/output to HSL')
    parser.add_argument('-hsv',  action='store_true', help='convert/output to HSV')
        
    parser.add_argument('-isHex',  action='store_true', help='indicate that inputted value(s) will be hex')
    parser.add_argument('-isRgb',  action='store_true', help='indicate that inputted value(s) will be sets of RGB codes')
    parser.add_argument('-isCmy',  action='store_true', help='indicate that inputted value(s) will be sets of CMY codes')
    parser.add_argument('-isCmyk', action='store_true', help='indicate that inputted value(s) will be sets of CMYK codes')
    parser.add_argument('-isHsl',  action='store_true', help='indicate that inputted value(s) will be sets of HSL codes')
    parser.add_argument('-isHsv',  action='store_true', help='indicate that inputted value(s) will be sets of HSL codes')
    
    parser.add_argument('--input',   '-i', help='name of the input file containing color codes to process')
    parser.add_argument('--output',  '-o', help='the name of a file to store output in (will create file if doesn\'t exist, will OVERWRITE existing file\'s contents)')
    parser.add_argument('--append',  '-a', action='store_true', help='append rather than overwrite when outputting to file rather than stdout')
    parser.add_argument('--verbose', '-v', action='store_true', help='print when performing conversions')
    
    parser.add_argument('color', nargs='*', help='a color in Hex, RGB, CMY, CMYK, HSL or HSV format')
    args = parser.parse_args()


    ''' PROCESS ARGS '''
    # determine which conversions to perform 
    outputFormats = []
    flagsActive = 0
    for flag in vars(args).keys() :
        # if the flag for an output type is present, keep trac
        if (vars(args).get(flag, False)) and (flag in TYPES) :
            flagsActive += 1
            outputFormats.append(flag)   
    # if no conversion flags specified, perform every format conversion
    if flagsActive == 0 :
        for colorFormat in TYPES :
            outputFormats.append(colorFormat)
        
    # determine if output should be (over?)written to file
    if args.output :
        global OUTPUT_DESTINATION
        OUTPUT_DESTINATION = args.output
        if not args.append :
            output_file = open(OUTPUT_DESTINATION, 'w')
            output_file.write('')
            output_file.close()

    # print conversion updates? 
    if args.verbose : 
        global VERBOSE
        VERBOSE = True


    ''' PARSE INPUTTED COLORS '''
    colorCodes = []
    # if provided a file of values
    if args.input :
        with open(args.input, 'r', encoding='utf-8') as file :
            for line in file :
                line = line.strip()
                if line != '' :
                    colorCodes.append(line)
    # else grab from stdin
    else :
        colorCodes = args.color    


    ''' PROCESS COLORS '''
    for color in colorCodes :
        # first check if input override has been provided 
        if args.isHex :
            handleHex(color, outputFormats)
        elif args.isRgb :
            handleRGB(color, outputFormats)
        elif args.isCmy :
            handleCMY(color, outputFormats)
        elif args.isCmyk :
            handleCMYK(color, outputFormats)
        elif args.isHsl :
            handleHSVorHSL(color, 'hsl', outputFormats)
        elif args.isHsv :
            handleHSVorHSL(color, 'hsv', outputFormats)
        # otherwise, attempt to automatically handle value 
        elif detectColorFormat(color, outputFormats) :
            continue
        else :
            print('ERROR: Could not detect inputted color format and no override format flag was provided. See --help for more information on usage.')
            return
    return


'''
# FORMAT HANDLERS
'''
# Handles a hex value's conversion and output
# ARGS
# color: string containing hex code
# outputFormats: list indicating which conversions to perform
def handleHex(color, outputFormats) :
    # validate/sanitize input
    hexcode = validateHex(color)
    if hexcode is None :
        return

    # convert and collect results
    results = {}
    if VERBOSE :
        results['verbose-msg'] = 'CONVERTING HEX: ' + hexcode

    rgbValues = HEXtoRGB(hexcode)
    for colorFormat in TYPES :
        if colorFormat in outputFormats and colorFormat == 'hex' :
            results['hex'] = hexcode
        elif colorFormat in outputFormats and colorFormat == 'rgb' :
            results['rgb'] = rgbValues
        elif colorFormat in outputFormats :
            results[colorFormat] = rgbTo(colorFormat, rgbValues)

    printConversions(results)


# Handles an RGB value's conversion and output
# ARGS
# color: string containing RGB code
# outputFormats: list indicating which conversions to perform 
def handleRGB(color, outputFormats) :
    # validate/sanitize input
    rgbValues = validateRGB(color)
    if rgbValues is None :
        return

    # convert and collect results
    results = {}
    if VERBOSE :
        results['verbose-msg'] = 'CONVERTING RGB: ' + str(rgbValues)
    
    for colorFormat in TYPES :
        if colorFormat in outputFormats and colorFormat == 'rgb' :
            results['rgb'] = rgbValues
        elif colorFormat in outputFormats :
            results[colorFormat] = rgbTo(colorFormat, rgbValues)
    
    printConversions(results)

# Handles a CMY value's conversion and output
# ARGS
# color: string containing CMY code
# outputFormats: list indicating which conversions to perform 
def handleCMY(color, outputFormats) :
    # validate/sanitize input
    cmyValues = validateCMYorCMYK(color, False) 
    if cmyValues is None :
        return

    # convert and collect results
    results = {}
    if VERBOSE :
        results['verbose-msg'] = 'CONVERTING CMY: ' + str(cmyValues)

    rgbValues = CMYtoRGB(cmyValues)
    for colorFormat in TYPES :
        if colorFormat in outputFormats and colorFormat == 'rgb' :
            results['rgb'] = rgbValues
        elif colorFormat in outputFormats and colorFormat == 'cmy' :
            results['cmy'] = cmyValues
        elif colorFormat in outputFormats :
            results[colorFormat] = rgbTo(colorFormat, rgbValues)

    printConversions(results)

# Handles a CMYK value's conversion and output
# ARGS
# color: string containing CMYK code
# outputFormats: list indicating which conversions to perform 
def handleCMYK(color, outputFormats) :
    # validate/sanitize input
    cmykValues = validateCMYorCMYK(color, True) 
    if cmykValues is None :
        return

    # convert and collect results
    results = {}
    if VERBOSE :
        results['verbose-msg'] = 'CONVERTING CMYK: ' + str(cmykValues)
 
    rgbValues = CMYKtoRGB(cmykValues)
    for colorFormat in TYPES :
        if (colorFormat in outputFormats) and (colorFormat == 'rgb') :
            results['rgb'] = rgbValues
        elif (colorFormat in outputFormats) and (colorFormat == 'cmyk') :
            results['cmyk'] = cmykValues
        elif colorFormat in outputFormats :
            results[colorFormat] = rgbTo(colorFormat, rgbValues)

    printConversions(results)

# Handles either an HSV or HSL value's conversion and output
# ARGS
# color: string containing CMY code
# outputFormats: list indicating which conversions to perform 
# handle: string ('hsl' or 'hsv'), indicating which format to handle 
def handleHSVorHSL(color, handle, outputFormats) :
    # sanitize/validate input
    validated = validateHSLorHSV(color)
    if validated is None :
        return

    # convert and collect results
    results = {}
    if VERBOSE :
        if handle == 'hsl' :
            results['verbose-msg'] = 'CONVERTING HSL: ' + str(validated)
        else :
            results['verbose-msg'] = 'CONVERTING HSV: ' + str(validated)
    
    rgbValues = HSLorHSVToRGB(validated, handle)
    for colorFormat in TYPES :
        if (colorFormat in outputFormats) and (colorFormat == 'rgb') :
            results['rgb'] = rgbValues
        elif (colorFormat in outputFormats) and (colorFormat == 'hsl') and (handle == 'hsl') :
            results['hsl'] = validated
        elif (colorFormat in outputFormats) and (colorFormat == 'hsv') and (handle == 'hsv'):
            results['hsv'] = validated
        elif colorFormat in outputFormats :
            results[colorFormat] = rgbTo(colorFormat, rgbValues)

    printConversions(results)



'''
# CONVERSION FUNCTIONS
'''

##
# RGB -> OTHER FORMATS SECTION 
###

# rgbTo() acts as an interface between format handlers and RGB conversions (for easier addition of formats later)
# ARGS
# colorFormat: a string containing a color format to convert to
# rgbValues: the rgbValues to convert
# RETURNS
# the converted color values in the specified format
def rgbTo(colorFormat, rgbValues) :
    if colorFormat == 'hex' :
        return RGBtoHEX(rgbValues)
    if colorFormat == 'cmy' :
        return RGBtoCMY(rgbValues)
    if colorFormat == 'cmyk' :
        return RGBtoCMYK(rgbValues)
    if colorFormat == 'hsl' :
        return RGBtoHSVorHSL(rgbValues, 'hsl')
    if colorFormat == 'hsv' :
        return RGBtoHSVorHSL(rgbValues, 'hsv')

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

# Takes in a list of 3 integers, returns a list of 3 floats (percentages)
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
        return [hue, saturation * 100, lightness * 100]
    else : # convert to HSV
        if value != 0 :
            saturation = chroma / value
        return [hue, saturation * 100, value * 100]


##
# OTHER FORMATS -> RGB SECTION
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
        R = chroma + m
        G = 0 + m
        B = x + m
        return [smartRound(R * 255), smartRound(G * 255), smartRound(B * 255)]
    else :
        print('RGB to HSV/HSL conversion failed')
        return


'''
# INPUT VALIDATION 
'''

# Takes in a string. 
# If string contains a valid Hex color code, it gets returned as a string.
def validateHex(value) :
    # attempt to extract hex code
    hexcode = extractValues(value, 1, True)

    if not hexcode :
        print('ERROR: Improper format for hex code (see --help)')
        return 

    return hexcode[0]

# Takes in a string. Returns same list as integers if valid RGB values. 
def validateRGB(color) :
    # extract 3 numbers from the provided values
    rgbValues = extractValues(color, 3)

    if not rgbValues : 
        print('ERROR: Improper format for RGB (see --help)')
        return

    intValues = []
    for value in rgbValues :
        value = smartRound(value)
        if (value < 0) or (value > 255) :
            print(f'ERROR: Each RBG value must be between 0-255, was {value}')
            return 
        intValues.append(value)
    
    return intValues

# Takes in a list of 3 or 4 strings. Returns same list as integers if valid CMYK values.
def validateCMYorCMYK(color, include_K) :
    k = ''
    if include_K :
        k = 'K'
        values = extractValues(color, 4)
    else :
        values = extractValues(color, 3)
    if not values :
        print(f'ERROR: Improper format for CMY{k} (see --help)') 
        return

    floatValues = []
    for value in values :
        value = float(value)
        if (value < 0) or (value > 100) :
            print(f'ERROR: Each CMY{k} value must be between 0.0-100.0, was {value}')
            return
        floatValues.append(value)
    
    return floatValues

# Takes in a list of 3 strings. Returns same list as 1 integer and 2 floats
def validateHSLorHSV(color) :
    color = extractValues(color, 3)
    if color is None :
        print(f'ERROR: Improper format for HSL/V (see --help)') 
        return

    for i in range(3) :
        if i == 0 :
            color[i] = smartRound(color[i])
        else :
            color[i] = float(color[i])

    if (color[0] < 0) or (color[0] > 360) :
        print(f'ERROR: Invalid H value (should be 0-360, was {color[0]})')
        return
    if (color[1] < 0) or (color[1] > 100) :
        print(f'ERROR: Invalid S value (should be 0.0-100.0, was {color[1]})')
        return
    if (color[2] < 0) or (color[2] > 100) :
        print(f'ERROR: Invalid V/L value (should be 0.0-100.0, was {color[2]})')
        return

    return [color[0], color[1], color[2]]


'''
# GENERAL UTILITIES
'''

# ARGS
# color: a string containing a color value in an unknown format
# outputFormats: a list containing information necessary for handling conversions, used if format is detected
# RETURNS
# truth if success, false if failure to detect a format
def detectColorFormat(color, outputFormats) :
    if 'rgb' in color.lower() :
        handleRGB(color, outputFormats)
        return True
    elif 'cmyk' in color.lower() :
        handleCMYK(color, outputFormats)
        return True
    elif 'cmy' in color.lower() :
        handleCMY(color, outputFormats)
        return True
    elif 'hsl' in color.lower() :
        handleHSVorHSL(color, 'hsl', outputFormats)
        return True
    elif 'hsv' in color.lower() :
        handleHSVorHSL(color, 'hsv', outputFormats)
        return True
    elif '#' in color :
        handleHex(color, outputFormats)
        return True
    else :
        return False


# Extracts numerical (hex or decimal) values from a string. 
# ARGS
# color: string containing value(s)
# numValues: determines how many values to extract (e.g. 3 for RGB, 4 for CMYK)
# isHex: determines if we're looking for hex rather than decimal
# RETURNS
# a list of extracted color/number values in string form (or false if faulure to extract)
def extractValues(color, numValues, isHex = False) :
    i = 0
    tempValue = ''
    extractedValues = []

    if isHex :
        # search for hex values
        while i < len(color) :
            if (color[i].isnumeric()) or (color[i] in HEX_LETTERS) :
                tempValue += color[i]
            else :
                tempValue = ''
            if len(tempValue) == 6 :
                extractedValues.append(tempValue)
                tempValue = ''
            if len(extractedValues) == numValues :
                break
            i = i + 1

        if (len(extractedValues) != numValues) and (len(tempValue) == 6) :
            extractedValues.append(tempValue)

    else :
        # search for decimal values
        while i < len(color) :
            if color[i].isnumeric() or color[i] == '.' :
                tempValue += color[i]
            elif len(tempValue) > 0 and tempValue != '.' :
                extractedValues.append(tempValue)
                tempValue = ''
            else :
                tempValue = ''
            if len(extractedValues) == numValues :
                break
            i = i + 1

        if (len(extractedValues) != numValues) and (len(tempValue) > 0) :
            extractedValues.append(tempValue)

    if len(extractedValues) != numValues :
        print(f'Could not extract the correct number of values from input: "{color}".\n- Number of values required: {numValues}\n- {len(extractedValues)} values successfully extracted: {extractedValues}')
        return False

    return extractedValues


# formats and delivers color values to STDOUT or a specified output file
# ARGS
# convertedValues: a map of the results from the color translations that were performed on a single color value, 
#                  where the key indicates the format and the value is a list of raw numeric values
def printConversions(convertedValues) :    
    output = []
    if VERBOSE : 
        output.append(convertedValues['verbose-msg'])
    
    # format converted values into better output strings
    for colorFormat in TYPES :
        if convertedValues.get(colorFormat, None) is None :
            continue
        elif colorFormat == 'hex' :
            hexCode = '#' + convertedValues['hex']
            output.append(hexCode) 
        else :
            # format strings for xyz(a,b,c) type formats
            colorCode = colorFormat + '('
            numValues = len(convertedValues[colorFormat])
            for valueIndex in range(numValues) :
                value = convertedValues[colorFormat][valueIndex]
                if type(value) == float :
                    value = f"{value:.2f}"
                if valueIndex == numValues - 1 :
                    colorCode += str(value) + ')'
                else :
                    colorCode += str(value) + ', '
            output.append(colorCode)
    
    # deliver formatted output
    if OUTPUT_DESTINATION != 'stdout' :
        
        ''' 
        TODO FOR EFFICIENCY:

        right now, unless i'm mistaken and there's some hidden python optimization going on, this is 
        going to open and close the file to write the conversions of each inputted color code.
        if there's a huge file being used as input, this may get slow, so perhaps the best move is
        to actually open the file back in main() at the point when we evaluate args, and then close
        it after everything in main() has ran... food for thought.
        '''
        with open(OUTPUT_DESTINATION, 'a', encoding='utf-8') as file :
            for color in output :
                file.write(color + '\n')
            file.write('\n')
    else :
        for color in output :
            print(color)
        print()

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



''' init '''
if __name__ == '__main__' :
    main()
