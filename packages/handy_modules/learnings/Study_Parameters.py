import sys

import argparse

def main(argv):
    parser = argparse.ArgumentParser(description='Using HDRTools')

    #positional argument as string
    parser.add_argument("file", help="the file name")

    parser.add_argument("-b","--color_container",choices=['BT2020', 'BT709'],default='BT2020', help="Color Container, either BT2020 or BT709")

    parser.add_argument("-e", "--usingEXR",action="store_true",help="Use EXR")

    #positional argument as type
    parser.add_argument("-y", type=int,choices=list(range(1, 4)), help="the exponent")

    #single argument one option as flag
    parser.add_argument("-x",help="use x for this",action="store_true")

    #optional parameter as string name is the argument name
    parser.add_argument("-t","--name",help=" add name ")


   #optional parameter as number, number is the argument name
    parser.add_argument("-s","--number",help=" add number ")

    #optional parameter as string now v is the name, but now is unclear in help
    parser.add_argument("-v",help=" add number ")


    parser.add_argument("-r", "--remove", action="store_true",help="remove")


    args = parser.parse_args(args=argv)
    if args.file:
      print(args.file)
    
    if args.x:
        print(" x is er ")
    else:
        print(" x is er niet")

    #print(args.remove)



if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

