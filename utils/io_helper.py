'''
Module delegated to file io
'''

def read_file(path: str) -> list:
    '''
    Reads each line of file and returns a list of strings
    '''
    res = []
    with open(path) as text_file:
        lines = text_file.readlines()
        for line in lines:
            res.append(line)
    return res

def write_file(path: str, buff: list):
    '''
    Write each line of the buffer into a new text file at a given path
    '''
    with open(path, 'w+') as text_file:
        for line in buff:
            text_file.write(line)
