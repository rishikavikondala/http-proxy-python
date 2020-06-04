#!/usr/bin/env python3

import datetime

def main():
    now = datetime.datetime.now()
    print(now.strftime('%d/%b/%Y:%H:%M:%S'))

if __name__=="__main__":
    main()