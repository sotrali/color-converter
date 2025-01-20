# color-converter

A CLI utility written in Python that translates color codes to other formats.

= actively under construction =

# Project Background

I started this project because I found myself converting between Hex and RGB a lot while ricing. As I was frequently visiting various color picker websites, I began thinking more and more about how color conversions even work in the first place.

Using any random color-picker online to go from RBG->Hex (and vice versa) works plenty fine, but I think CLI tools are cool, and I couldn't find any CLI color conversion utilities.

# Usage

This program supports hexcodes, RGB, CMY, CMYK, HSL, and HSV.

Simply supply a color in any of the supported formats as a string, and you will receive the equivalent color codes in all of the supported formats.

For example, a simple input with all conversions:

```
$ python color-converter.py "#85feab"
#85feab
rgb(133, 254, 171)
cmy(47.84, 0.39, 32.94)
cmyk(47.64, 0.00, 32.68, 0.39)
hsl(138.84, 98.37, 75.88)
hsv(138.84, 47.64, 99.61)
```

You can use flags to limit the output:

```
$ python color-converter.py -cmy -hsv "#85feab"
cmy(47.84, 0.39, 32.94)
hsv(138.84, 47.64, 99.61)
```

---

It can also function as a color translation utility for converting colors in bulk.

It can handle more than one input on the command line, or you can input files. You can limit the output to one or more specific formats.
For example, you could take a file that has color codes on each line, each in different formats, and have them all converted to a single format.

For example, use this command:

```
$ python color-converter -cmyk -i "input_file" -o "output_file"
```

where the input file contains:

```
rgb(1, 2, 3)
#123456
HSV(1, 2, 3)
```

and the output file is populated with:

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
"  rgb: 100 200 300"
"rGb-100 .   200^300"
```

_Note: Hexcodes will require a '#' in order to be automatically recognized._

While the program will always try to auto-detect the input format, If you only have raw number values, you can specify a fallback format with flags.

For example:

```
$ python color-converter.py -rgb -isHex "123abc"
rgb(18, 58, 188)

// or

$ python color-converter.py -hsl -isCmy "12 32 90"
#e0ad19
rgb(224, 173, 25)
cmy(12.00, 32.00, 90.00)
cmyk(0.00, 22.77, 88.84, 12.16)
hsl(44.62, 79.92, 48.82)
hsv(44.62, 88.84, 87.84)
```

(Don't forget to use the `-h` or `--help` flags for in-terminal help)

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
