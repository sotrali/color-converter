def extractValues(color, numValues, isHex = False) :
    print(color)
    i = 0
    tempValue = ''
    extractedValues = []

    if isHex :
        # search for hex values
        hexCharacters = ['a', 'b', 'c', 'd', 'e', 'f']
        while i < len(color) :
            if (color[i].isnumeric()) or (color[i] in hexCharacters) :
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
            elif len(tempValue) > 0 :
                extractedValues.append(tempValue)
                tempValue = ''
            if len(extractedValues) == numValues :
                break
            i = i + 1

        if (len(extractedValues) != numValues) and (len(tempValue) > 0) :
            extractedValues.append(tempValue)

    if len(extractedValues) != numValues :
        print(f'Could not extract the desired number of values from input. Values requested: {numValues}, values extracted: {len(extractedValues)}, {extractedValues}')
        return False

    print(extractedValues)
    return

def main() :

    # hexcolor1 = '123abc'
    # hexcolor2 = 'zx123abc def654'
    # hexcolor3 = 'test sentence with hex in it: 123456, 654321, abc123, aefacd'

    # extractValues(hexcolor1, 1, True)
    # extractValues(hexcolor2, 1, True)
    # extractValues(hexcolor2, 2, True)
    # extractValues(hexcolor3, 4, True)

    color1 = 'cmy(123, ba12.4,   51 )'
    color2 = 't3st 123 456'
    color3 = '1.23 word 3,2 1.34'

    extractValues(color1, 3)
    


if __name__ == '__main__' :
    main()