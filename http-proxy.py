#!/usr/bin/env python3

# add import statements here
import argparse

# define classes, enums, etc here

# define functions here

def main():
    # register arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help='TCP port for HTTP proxy', default=9999)

    # parse the command line
    args = parser.parse_args()

    


            

            



# if statement so main() runs by default from command line
if __name__=="__main__":
    main()