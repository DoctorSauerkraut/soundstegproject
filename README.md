# soundstegproject
Steganography tools for audio files

The purpose of this tool is to apply/extract a watermark (contained in an input file) from a given wav file. The watermark can be integrated with LSB (key-mapped) or DSS (Spread-Spectrum) technique.

Usage
Type main.py -h for options

Commands: 
r read a tag from input sound file
w write a tag in a sound file
atk attack a sound file with various effects
cmp compare files (do not confuse it with the diff script)
e evaluate the required time to bruteforce the tag


We did integrate a diff algorithm to compare signals under attack

Implemented algorithms :
Classic LSB
Mapped LSB
Direct Spread Spectrum

Implemeted attacks:
Echo effect