# color-converter

A robust CLI color conversion utility written in Python.

# Features

- Supports conversions between hexcode, RGB, CMY, CMYK, HSL, and HSV
- Lenient automatic input detection
- Bulk conversions to and from files

# Usage

Simply supply one or more colors in any of the supported formats as a string, and it will perform all supported conversions.

```
$ python color-converter.py "#85feab"
#85feab
rgb(133, 254, 171)
cmy(47.84, 0.39, 32.94)
cmyk(47.64, 0.00, 32.68, 0.39)
hsl(138.84, 98.37, 75.88)
hsv(138.84, 47.64, 99.61)
```

You can also use flags to limit the output:

```
$ python color-converter.py -rgb "#abc123" "#def456"
rgb(171, 193, 35)

rgb(222, 244, 86)

```

---

It can also function as a color translation utility for converting colors in bulk.

For example, you could take a file that has color codes in various formats and have them all converted to a single format.

To do what was just described, use this command:

```
$ python color-converter -cmyk -i "input_file" -o "output_file"
```

where the input file contains:

```
rgb(1, 2, 3)
#123456
HSV(1, 2, 3)
```

and the output file gets populated with:

```
cmyk(66.67%, 33.33%, 0%, 98.82%)
cmyk(79.07%, 39.53%, 0%, 66.27%)
cmyk(0%, 1.97%, 2%, 97%)
```

_Note: include the `-a` flag to append to the specified output file, rather than overwriting it._

---

The program attempts to determine what color format you're inputting, and will succeed as long as the format is indicated at some point in the input string.

For example, these are all valid strings to input 100, 200, and 300 as RGB values:

```
"rgb(100, 200, 300)"
"  RGB: 100 200 300"
"rGb-100 .   200^300"
```

_Note: Hexcodes will require a '#' in order to be automatically recognized._

While the program will always try to auto-detect the input format, If you only have raw number values, you can specify a fallback format with flags.

For example:

```
$ python color-converter.py -rgb -isCmyk "1 2 3 4"
rgb(242, 240, 237)
```

(Don't forget to use the `-h` or `--help` flags for in-terminal help)

# Project Background

I started this project because I found myself converting between Hex and RGB a lot while ricing. As I was frequently visiting various color picker websites, I began thinking more and more about how color conversions even work in the first place.

Using any random color-picker online to go from RBG->Hex (and vice versa) works plenty fine, but I think CLI tools are cool, and I couldn't find any CLI color conversion utilities.

# Conversion Sources

Hex<->RGB:

https://en.wikipedia.org/wiki/Web_colors

RGB<->CMYK:

https://www.101computing.net/cmyk-to-rgb-conversion-algorithm/

https://thecolorsmeaning.com/rgb-to-cmyk/

RGB<->CMY:

http://colormine.org/convert/rgb-to-cmy

RGB<->HSL:

https://www.baeldung.com/cs/convert-color-hsl-rgb

https://en.wikipedia.org/wiki/HSL_and_HSV#HSV_to_RGB
