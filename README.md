# soundstegproject
Steganography tools for audio files

The purpose of this tool is to apply/extract a watermark (contained in an input file) from a given wav file. The watermark can be integrated with LSB (key-mapped) or DSS (Spread-Spectrum) technique.

Usage
Writing : python main.py w <wavfile> <keyfile> <wmkfile>
Reading : python main.py r <wavfile> <keyfile>
Writing with DSS : python main.py lw <wavfile> <wmkfile>
Reading with DSS : python main.py lr <wavfile>
Applying effects : python main.py a <wavfile>