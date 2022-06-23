
from typing import NamedTuple
import re
from prettytable import PrettyTable

class TOKENIZER(NamedTuple):
    TOKEN: str
    lEXEMA: str
    line: int
    column: int

def tokenize(code):
    keywords = ['and', 'for', 'if', 'else', 'is', 'break','try', 'not',
                'import', 'continue', 'return', 'from', 'while',  'print',
                 'def', 'in',  'or']
    token_specification = [
        ('Numero',   r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN',   r'='),           # Assignment operator
        ('Compare', r':='),
        ('SeparadorComa',      r','),            # Statement terminator
        ('OperadorDiv',r'/'),
        ('OperadorMul',r'\*'),
        ('ID',       r'[A-Za-z]+'),    # Identifiers
        ('OPSUM',       r'[+]'),      # Arithmetic operators
        ('OPRES',       r'[\-]'),
        ('ParenIzq',    r'[(]'),
        ('ParenDer',    r'[)]'),
        ('LlaveIzq', r'[{]'),
        ('LlaveDer', r'[}]'),
        ('mayorQue', r'[>]'),
        ('menorQue', r'[<]'),
        ('NEWLINE',     r'\n'),        # Line endings
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH', r'.'),            # Any other character
    ]
    x = PrettyTable()
    ID = ""
    x.field_names = ["TOKEN/ID TOKEN", "LEXEMA","LINEA","COLUMNA"]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'Numero':
            value = float(value) if '.' in value else int(value)
            kind = 'NUMBER, ID TOKEN #1'

        elif kind == 'ASSIGN':
            kind = 'ASSIGN, ID TOKEN #5'

        elif kind == 'OPRES' and value == '-':
            kind = 'OPRES, ID TOKEN #11'

        elif kind == 'OperadorDiv' and value == '/':
            kind = 'OperadorDiv, ID TOKEN #12'

        elif kind == 'OperadorMul' and value == '*':
            kind = 'OperadorMul, ID TOKEN #13'

        elif kind == 'OPSUM' and value == '+':
            kind = 'OPSUM, ID TOKEN #14'

        elif kind == 'ParenIzq' and value == '(':
            kind = 'ParenIzq, ID TOKEN #6'

        elif kind == 'ParenDer' and value == ')':
            kind = 'ParenDer, ID TOKEN #7'

        elif kind == 'LlaveIzq' and value == '{':
            kind = 'LlaveIzq, ID TOKEN #8'

        elif kind == 'LlaveDer' and value == '}':
            kind = 'LlaveDer, ID TOKEN #9'

        elif kind == 'Compare' and value == ':=':
            kind = 'Compare, ID TOKEN #10'

        elif kind == 'menorQue' and value == '<':
            kind = 'menorQue, ID TOKEN #30'

        elif kind == 'mayorQue' and value == '>':
            kind = 'MayorQue, ID TOKEN #31'

        elif kind == 'ID' and value in keywords[16]:
            kind = value and "Palabra reservada, ID TOKEN #29"

        elif kind == 'ID' and value in keywords[15]:
            kind = value and "Palabra reservada, ID TOKEN #28"

        elif kind == 'ID' and value in keywords[14]:
            kind = value and "Palabra reservada, ID TOKEN #27"

        elif kind == 'ID' and value in keywords[13]:
            kind = value and "Palabra reservada, ID TOKEN #26"

        elif kind == 'ID' and value in keywords[12]:
            kind = value and "Palabra reservada, ID TOKEN #25"

        elif kind == 'ID' and value in keywords[11]:
            kind = value and "Palabra reservada, ID TOKEN #24"

        elif kind == 'ID' and value in keywords[10]:
            kind = value and "Palabra reservada, ID TOKEN #23"

        elif kind == 'ID' and value in keywords[9]:
            kind = value and "Palabra reservada, ID TOKEN #22"

        elif kind == 'ID' and value in keywords[8]:
            kind = value and "Palabra reservada, ID TOKEN #21"

        elif kind == 'ID' and value in keywords[7]:
            kind = value and "Palabra reservada, ID TOKEN #20"

        elif kind == 'ID' and value in keywords[6]:
            kind = value and "Palabra reservada, ID TOKEN #19"

        elif kind == 'ID' and value in keywords[5]:
            kind = value and "Palabra reservada, ID TOKEN #18"

        elif kind == 'ID' and value in keywords[4]:
            kind = value and "Palabra reservada, ID TOKEN #17"

        elif kind == 'ID' and value in keywords[3]:
            kind = value and "Palabra reservada, ID TOKEN #16"

        elif kind == 'ID' and value in keywords[2]:
            kind = value and "Palabra reservada, ID TOKEN #2"

        elif kind == 'ID' and value in keywords[1]:
            kind = value and "Palabra reservada, ID TOKEN #4"

        elif kind == 'ID' and value in keywords[0]:
            kind = value and "Palabra reservada, ID TOKEN #15"

        elif kind == 'ID':
            kind = value and "IDEN, ID TOKEN #3"

        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield TOKENIZER(kind, value, line_num, column)
        x.add_row([kind,value,line_num,column])

    print("")
    print("          Organización en prettyTable ")
    print("")
    print("--------------------PrettyTable-------------------")
    print(x)

archivo = open ('Prueba.py','r')
linea = archivo.read()

for token in tokenize(linea):
    print(token)