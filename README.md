# TODO

fix extractor, get hex working

# color-converter

A CLI utility written in Python that translates color codes to other formats.

= actively under construction =

# Usage

Download the python file and run it! Requires nothing besides vanilla Python :)

I'll flesh 'usage' README out later, but for now, use the help menu:
`python color-converter.py --help`

# Project Goals

I started this project because I found myself converting between Hex and RGB a lot while ricing my Arch setup, which got me thinking about how all of these conversion websites work.

Using any random color-picker online to go from RBG->Hex (and vice versa) works plenty fine, but I started to wonder if there was a simple program to do said conversions offline. Something that was fast, doesn't require internet/no ads, etc. I poked around on the AUR for any sort of CLI color converting utility, and couldn't find anything... At this point, I realized it was up to me!

# Roadmap

I originally just wanted this to be an exercise in Python that teaches me about color conversions and can do HEX <-> RGB. I've since decided to flesh it out and try to make it into something that could prove useful. My goal is to polish and post this around in the hopes other people find it helpful.

TODO:

- automatic format detection, no longer requiring a flag to indicate what format input is
- accept more than one color code at a time (-f for file input, -l for multiple (list of) strings
- (to expand on ^) accept input from text file, where each line is it's own color code to convert
- add flags to control which conversions are output (in the case you only want a single conversion) and how (do you want just the raw values or the whole string for with commas and stuff?)
- combine the last two bullet points and boom: now the tool could take a whole list of colors in X format and spit out a file where every color is in Y format
- (to expand on ^) if we had automatic format detection and formatting output flags, you could pass in a whole file of any color formats and standardize them to a given format.
- finish the color value extractor

# ENVISIONED USAGE:

in its simplest form, this program takes in a color code and prints out all of the equivalent color codes in the different supported formats (Hex, RGB, CMY, CMYK, HSL, HSV).

It can also function as a color translation utility for converting colors in bulk. It can handle more than one input on the command line (or you can input files) and you can limit the output to one or more specific formats.
For example, you could take a file that has color codes on each line, each in different formats, and have them all converted to a single format.

TODO: UPDATE THIS EXAMPLE
For example, input this file:

```
rgb(1, 2, 3)
#123456
HSV(1, 2, 3)
```

and receive this file:

```
cmyk(66.67%, 33.33%, 0%, 98.82%)
cmyk(79.07%, 39.53%, 0%, 66.27%)
cmyk(0%, 1.97%, 2%, 97%)
```

with this command:

> `$ python color-converter -cmyk -i input_file -o output_file`

_FURTHER TIPS / EXPLANATION:_

From the command line, the program accepts input colors as strings wrapped in quotes. The sanitization is pretty robust and unopinionated when it comes to formatting, as long as the format is indicated at some point in the string.

> Example valid RGB inputs:  
> `$ python color-converter "rgb(1, 2, 3)"`  
> `$ python color-converter "rgb(1 2 3)"`  
> `$ python color-converter "rgb1 2 3"`

The program will always try to automatically determine what format you entered.

> The sole exception to this is if you specify the input format. This is done when passing the program integers rather than strings. For example, to pass in raw RGB inputs and convert them to HSL:  
> `$ python color-converter -rgb -hsl 1 2 3`

- If you have multiple colors to convert, it may be faster to put them in a file than individually wrap them in quotes.

- If you're only inputting one value, you can

_For a single input to all available formats_:
`$ python color-converter "input_color"`

_For a single input to a specific format_:
`$ python color-converter -output_format "input_color"`

_For input(s) from command line to all available formats_:
`$ python color-converter "input_color1" "input_color2" "input_color3"`

## Conversion Sources

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
