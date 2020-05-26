def parse_line(data, encoding = 'iso-8859-1'):
    fields = data.partition(b'\n')

    if len(fields[1]) == 0:
        return None, data
    
    line = fields[0].rstrip(b'\r')
    line = line.decode(encoding)
    
    if len(fields[2]) == 0:
        return line, None
    
    return line, fields[2]

data = b''
with open("resources/response.http", "rb+") as f:
    data = f.read()

try:
    line, unparsed = parse_line(data)
    fields = line.split(' ', 2)
    print(fields)

    line, unparsed = parse_line(unparsed)
    while line != '':
        if line is None:
            raise Exception

        print(line)
        line, unparsed = parse_line(unparsed)

    print("SUCCESS")
except:
    print("FAIL")