'''
Module delegated to file io
'''
 
def read_file(path: str) -> list:
    '''
    Reads each line of file and returns a list of strings
    '''
    res = []
    with open(path) as text_file:
        res.append(text_file.readlines())
    return res

def write_file(path: str, buff: list):
    '''
    Write each line of the buffer into a new text file at a given path
    '''
    with open(path, 'w+') as text_file:
        for line in buff:
            print(line.strip())
