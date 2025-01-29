# color-converter

A robust CLI color conversion utility written in Python.

# Features

- Supports conversions between hexcode, RGB, CMY, CMYK, HSL, and HSV
- Lenient automatic input detection (can be overriden)
- Bulk conversions to and from files

# Usage

Simply supply one or more color codes in any of the supported formats as a string, and you will receive output of all supported format conversions.

```
$ python color-converter.py "#85feab"
#85feab
rgb(133, 254, 171)
cmy(47.84, 0.39, 32.94)
cmyk(47.64, 0.00, 32.68, 0.39)
hsl(138.84, 98.37, 75.88)
hsv(138.84, 47.64, 99.61)
```

You can use one or more flags to specify the output formats:

```
$ python color-converter.py -rgb -hsl "#abc123" "#def456"
rgb(171, 193, 35)
hsl(68.35, 69.30, 44.71)

rgb(222, 244, 86)
hsl(68.35, 87.78, 64.71)
```

---

You can also use this tool to convert codes in bulk.

For example, to input a file that has color codes in various formats and have them all converted to a single format:

```
$ python color-converter -cmyk -i "input_file" -o "output_file"
```

Where the input file contains:

```
rgb(1, 2, 3)
#123456
HSV(1, 2, 3)
```

If the output file didn't already exist, it will be created. Otherwise, it will be overwritten with:

```
cmyk(66.67, 33.33, 0.00, 98.82)

cmyk(79.07, 39.53, 0.00, 66.27)

cmyk(0.00, 12.50, 12.50, 96.86)

```

_Note: include the `-a` flag to append to an existing output file, rather than overwriting it._

---

The program will try to determine what color format you're inputting, and will succeed as long as the format is indicated at some point in the input string.

For example, these are all valid strings to input 50, 100, and 200 as RGB values:

```
"rgb(50, 100, 200)"
"  RGB: 50 100 200"
"excessive_stuff to! emphasize $ robsustness(rGb-50 .   )100^200"
```

_Note: Hexcodes need to start with '#' in order to be detected_ 

However, if you only have raw number values (or just want to manually override the auto detector), you can specify your input color format with flags.

For example:

```
$ python color-converter.py -rgb -isCmyk "1 2 3 4"
rgb(242, 240, 237)
```

(Don't forget to use the `-h` or `--help` flags for additional in-terminal help)

# Project Background

I started this project because I found myself converting between Hex and RGB a lot while ricing. As I was frequently visiting various color picker websites, I began thinking more and more about how color conversions even work in the first place. What is a color space?

Using any random color-picker online to go from RBG->Hex (and vice versa) works plenty fine, but, I think CLI tools are cool. I searched around a bit on github and the AUR and couldn't find any CLI color conversion utilities. I decided I could make one for fun, and the scope slowly expanded. I realized this was my opportunityto make and distribute a tool that could potentially serve others!

# Conversion Sources

Hex<->RGB:

https://en.wikipedia.org/wiki/Web_colors

RGB<->CMYK:

https://www.101computing.net/cmyk-to-rgb-conversion-algorithm/

https://thecolorsmeaning.com/rgb-to-cmyk/

RGB<->CMY:

http://colormine.org/convert/rgb-to-cmy

RGB<->HSL/HSV:

https://www.baeldung.com/cs/convert-color-hsl-rgb

https://en.wikipedia.org/wiki/HSL_and_HSV#HSV_to_RGB
