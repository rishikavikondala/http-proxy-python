#!/usr/bin/env python3

import argparse
# add additional import statements here

def main():
    # register arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help='TCP port of Echo Server', default=9999)
    parser.add_argument('text', type=str, help='UTF-8 text to send to echo server')

    # parse the command line
    args = parser.parse_args()
    message = args.text

    # ESTABLISH SOCKET AND CLIENT CONNECTION

    # SEND MESSAGE

    # RECEIVE RESPONSE

    # EXAMINE RESPONSE
    print('INPUT: {}'.format(message))
    print('RESPONSE: {}'.format(response))
    print('UTF-8 ENCODING: {}'.format('TODO'))) # Encode response as UTF-8

# if statement so main() runs by default from command line
if __name__=="__main__":
    main()