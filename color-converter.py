import sys
import argparse

TYPES = ['hex', 'rgb', 'hsl', 'cmyk']
HEX_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hex', action='store_true', help='convert from hex (accepted formats: [ffffff] or ["#ffffff"])')
    parser.add_argument('--rgb', action='store_true', help='convert from RGB (accepted formats: [R G B], [\"rgb(R, G, B)\"], and [\"rgb(R,G,B)\"])')
    parser.add_argument('color', nargs='*', help='accepts a color in Hex, RGB, CYMK, or HSL and performs format conversions')
    args = parser.parse_args()

    print('TYPES: ', TYPES)
    print(args)

    color = args.color 

    if len(color) == 0 :
        print('ERROR: Must enter color code')
        return

    # HANDLE HEX INPUT
    if args.hex :
        color = color[0].strip('#')
        if not validateHex(color) :
            return

        convertFromHex(color)

    # HANDLE RGB INPUT
    if args.rgb :
        # cleanse any non-numerical stuff
        if len(color) == 1 :
            color = color[0].strip('rgb(').strip(')').split(',')
        if not validateRGB(color) :
            return
        
        for i in range(len(color)) :
            color[i] = int(color[i])

        convertFromRGB(color)
        
##
# HEX CONVERSION SECTION
##

# Takes in valid RGB code and converts it to the other formats
def convertFromHex(hexCode) :
    print('-> Hex received: ', hexCode, ' ', type(hexCode))
    convertToRGB('hex', hexCode)
    # convertToCMYK('hex', code)
    # convertToHSL('hex', code)

def convertToHex(codeFormat, code) :
    hexValue = '#'
    
    if codeFormat == 'rgb' :
        for rgbValue in code :
            hexValue += hex(int(rgbValue / 16)) 
            hexValue += hex(int(rgbValue % 16))
    
    print('HEX: ', hexValue)


##
# RGB CONVERSION SECTION
##

# Takes in valid RGB code and converts it to the other formats
def convertFromRGB(code) :
    print('-> RGB received: ', code, ' ', type(code[0]), type(code[1]), type(code[2]))
    convertToHex('rgb', code)
    # convertToCMYK('rgb', code)
    # convertToHSL('rgb', code)

def convertToRGB(codeFormat, code) :
    if codeFormat == 'hex' :
        print('bsdfljbsdfb')

##
# INPUT VALIDATION SECTION
##

# Takes in a string. Returns True if valid Hex color code.
def validateHex(value) :
    if len(value) != 6 :
        print('ERROR: Hex value should have 6 digits')
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


# Takes in a list of numerical strings. Returns True if valid RGB values. 
def validateRGB(values) :
    if len(values) != 3 :
        print('ERROR: Improper number of values (should be 3)')
        return False

    for value in values :
        if not value.strip().isnumeric() :
            print('ERROR: Improper format for RGB value(s)')
            return False
        value = int(value)
        if (value < 0) or (value > 255) :
            print('ERROR: Each RBG value must be between 0-255')
            return False
    return True

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
