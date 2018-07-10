#!env python3

# Hex-B-Gone
# Change "\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64" to "Hello World"
import sys
import re
usage = """Usage: ./hexbgon.py <infile> [outfile]
Examples:
./hexbgon.py somefile{.js,.nohex.js}
./hexbgon.py somefile.js somefile.nohex.js
Output defaults to <infile>.HBG.js if not specified"""

# open file
filename = "" 
if (len(sys.argv) > 1):
    filename = sys.argv[1]
    try:
       file = open(filename)
       print("Parsing "+filename+"...", end="")
    except Exception as e:
        print("File not found:"+filename)
        quit()
else:
    print(usage)
    quit()

flines = file.read()
file.close()

# replace ascii-hex with regular ascii
def decode(str):
    hexval = bytearray.fromhex(str)

    if(hexval[0] < 0x20):
        return str
    elif(hexval[0] in (0x5c, 0x22, 0x27)): # \, ", '
        return "\\"+hexval.decode()
    else:
        return hexval.decode()

r = re.sub(
    r"(\\x)(\w{2})",
    lambda s: decode(s.group(2)),
    flines)

# write new file
if(len(sys.argv) > 2):
    outfilename = sys.argv[2]
else:
    outfilename = re.sub(r".js", r".HBG.js", filename)

with open(outfilename, 'w') as outfile:
    try:
        outfile.write(r)
        print("Done.")
    except Exception as e:
        print("Could not write "+outfilename)
        quit()
