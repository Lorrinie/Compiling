import re

char_dict = {
    "#": 0,
    "main": 1,
    "if": 2,
    "then": 3,
    "while": 4,
    "do": 5,
    "static": 6,
    "int": 7,
    "double": 8,
    "struct": 9,
    "break": 10,
    "else": 11,
    "long": 12,
    "switch": 13,
    "case": 14,
    "typedef": 15,
    "char": 16,
    "return": 17,
    "const": 18,
    "float": 19,
    "short": 20,
    "continue": 21,
    "for": 22,
    "void": 23,
    "sizeof": 24,
    "ID": 25,
    "NUM": 26,
    "+": 27,
    "-": 28,
    "*": 29,
    "/": 30,
    ":": 31,
    ":=": 32,
    "<": 33,
    "<>": 34,
    "<=": 35,
    ">": 36,
    ">=": 37,
    "=": 38,
    "default": 39,
    ".": 40,
    ";": 41,
    "(": 42,
    ")": 43,
}


def get_text(path):
    """get text from the given path

    :param path: str
    :rtype: code in the path
    """
    with open(path) as file_object:
        text = file_object.read()
    return text


def remove_unprintable_characters(text):
    """remove unprintable characters and comments, return the processed data

    :param text: unprocessed data
    :rtype: processed data
    """
    operators = ('+', '-', '*', '/', ':', '=', '<', '>', '#', ';', '(', ')')
    uncommon = (':', '<', '>')
    flag = 0
    new_text = ''
    tmp = ''

    text = re.sub(r'//.*', ' ', text)           # remove single-line comments
    text = re.sub(r'\n+|\r+|\t+', ' ', text)    # remove unprintable characters
    text = re.sub(r'/\*.*?\*/', ' ', text, flags=re.S)   # remove multi-line comments

    for c in text:
        if c in operators:
            if c in uncommon and flag == 0:
                flag = 1
                new_text += ' ' + c
                tmp = c
            elif flag == 1 and is_complex_operator(tmp, c):
                new_text += c + ' '
                flag = 0
            else:
                new_text += ' ' + c + ' '
                flag = 0
        elif flag == 1:
            new_text += ' ' + c
            flag = 0
        else:
            new_text += c
            flag = 0
    # print(new_text)
    new_text = re.sub(r' +', ' ', new_text)
    return new_text.strip()


def is_complex_operator(a, b):
    op = a + b
    if op == ':=' or op == '<=' or op == '>=' or op == '<>':
        return True
    return False


def generate_list(text):
    """generate a list contain symbols

    :param text: str
    :rtype: list

    """
    symbol_list = text.split(" ")
    return symbol_list


def classify(slist):
    """classify the symbols from slist

    :param slist: list

    """
    sid = re.compile('^[a-zA-Z]\w*$')
    num = re.compile('^\d+$')

    # print(slist)
    for i, element in enumerate(slist):
        if element in char_dict:
            slist[i] = "< " + element + " , " + str(char_dict[element]) + " >"
        elif sid.match(element):
            slist[i] = "< '" + element + "' , 25 >"
        elif num.match(element):
            slist[i] = "< " + element + " , 26 >"
        else:
            slist[i] = "< error >"


def print_element(slist):
    """print the element from slist"""
    for element in slist:
        print(element)


def main():
    """main function"""
    file_name = "test.txt"
    text = get_text(file_name)
    processed_text = remove_unprintable_characters(text)
    slist = generate_list(processed_text)
    classify(slist)
    print_element(slist)


if __name__ == '__main__':
    main()
