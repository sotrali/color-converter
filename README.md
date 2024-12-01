# color-converter
A CLI utility written in Python that translates color codes to other formats.

= actively under construction =

# Usage
Download the python file and run it! Requires nothing besides vanilla Python :)

I'll flesh 'usage' README out later, but for now, use the help menu:
`python color-converter.py --help` 

# Project Goals
I started this project because I found myself converting between Hex and RGB a lot while ricing my Arch setup and I started thinking about the available color tools. Using any random color-picker site (or the ones baked into search engines) to go from RBG->Hex (and vice versa) work plenty fine, but I started to wonder if there was a simple way to do said conversions locally. Something that was super quick, doesn't require internet, and doesn't have any fluff. I poked around on the AUR for any sort of CLI color code converting utility, and couldn't find anything. At this point, I had the realization that I had no idea how color codes work, and that it could be a fun way to learn something new by making one myself. 

Also, up til this point, I had no personal projects written in Python (which is a language I'm trying to learn quickly for my job), and I had always wanted to write a legit CLI tool. So, how about 4 birds in one stone?


# Roadmap
I originally (and still) just want this to be an exercise in Python that results in a somewhat useful tool. I would like to get it to a level of polish where I'm proud to release it with the MIT license or something and have it on the AUR.

That said, as I develop this, I see lots of room for improvement. Such as:
- automatic format detection, no longer requiring a flag to indicate what format input is
- accept more than one color code at a time
- (to expand on ^) accept input from text file, where each line is it's own color code to convert
- add flags to control which conversions are output (in the case you only want a single conversion) and how (do you want just the raw values or the whole string for with commas and stuff?)
- combine the last two bullet points and boom: now the tool could take a whole list of colors in X format and spit out a file where every color is in Y format
- (to expand on ^) if we had automatic format detection and formatting output flags, you could pass in a whole file of any color formats and standardize them to a given format.


maybe these ideas branch off into separate projects themselves, but:
- accept images as output and print out the average color (of all pixels) in any format
- TUI color picker??? maybe look into the interface platforms that ncspot uses for mouse input
- accept images as output and some sort of color code that gets applied to said image (like a CLI program for applying color filters to images)

## Conversion Sources
Hex<->RGB: https://en.wikipedia.org/wiki/Web_colors

RGB<->CMYK: https://thecolorsmeaning.com/rgb-to-cmyk/
