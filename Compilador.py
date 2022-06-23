# LIBRERÍAS PARA EXPRESIONES REGULARES Y ORGANIZACIÓN DE TABLA VISUAL PARA TOKENS

from typing import NamedTuple
import re
from prettytable import PrettyTable
import tkinter as tk
from tkinter import filedialog
import PySimpleGUI as sg
from tkinter import messagebox


# En esta clase Analizador se hará el desarrollo de un analiador léxico-gráfico
# Partiendo de una tabla de palabras claves y símbolos predefinida
# Se cuenta con múltiples métodos tales como:
# __init__(this)
# read_file(this, file)
# write_file(this, lineas, file)
# get_token(this, linea)
# run(this, linea, flag=True)
# Contando cada uno con su respectivo funcionamiento dentro del código

class Analizador(object):

    # En la clase __init__(this) se realiza la inicialización de tipos importantes, por medio de expresiones regulares,
    # así como el establecimiento de la lista de palabras clave
    def __init__(this):

        # Número de línea
        this.lineno = 1

        # Establecimiento de palabras clave
        this.palabraReservada = ['and', 'for', 'if', 'else', 'is', 'break', 'pass',
                                 'try', 'not', 'import', 'continue', 'return', 'from', 'while', 'yield', 'print',
                                 'with', 'def', 'in', 'global', 'or', 'except']

        # inicialización de palabras claves
        palabraReservada = r'(?P<palabraReservada>(and){1}|(for){1}|(if){1}|(else){1}|' \
                           r'(is){1}|(break){1}|(pass){1}|(try){1}|(not){1}' \
                           r'(import){1}|(continue){1}|(return){1}|(from){1}|(while){1}' \
                           r'(yield){1}|(print){1}|(with){1}|(def){1}|' \
                           r'(in){1}|(global){1}|(or){1}|(except){1})'

        # inicialización de operadores
        Operador = r'(?P<Operador>\+|\+|\+=|-|\*|/|%|<|>)'

        # inicialización de caracter de asignación
        Assign = r'(?P<Assign>\+|:=|==)'

        ##inicialización de separadores
        Separador = r'(?P<Separador>[,:{}:)(.] )'

        # numeros únicamente en forma flotante ejemplo= 1.0,5.6
        Numero = r'(?P<Numero>\d+(\.\d*)?)'

        # Una variable no puede ser nombrada con nombres de palabras reservadas
        # Por tanto, todo símbolo que no esté definido será identificador
        ID = r'(?P<ID>[a-zA-Z_][a-zA-Z_0-9]*)'

        Error = r'\"(?P<Error>.*)\"'

        # Comentario ^ Inicio de la línea de coincidencia. Coincidir con cualquier carácter que no sea nueva línea \ r retorno de carro \ n nueva línea
        Comentario = r'(?P<Comentario>/\*(.|[\r\n])*/|#[^\n]*)'

        # Ensamblar las expresiones regulares anteriores de una manera lógica, en un cierto orden lógico
        # La función de compilación se usa para compilar expresiones regulares y generar un objeto de expresión regular
        this.patterns = re.compile(
            '|'.join([Comentario, palabraReservada, ID, Numero, Separador, Operador, Error, Assign]))

    # Funcion para leer el archivo
    def read_file(this, file):
        with open(file, "r") as f_input:
            return [linea.strip() for linea in f_input]

    # Función para empezar a imprimir en pantalla la tabla de símbolos
    def run(this, linea, flag=True, ):
        for token in this.get_token(linea):
            if flag:
                print("linea %3d :" % this.lineno, token)

    def get_token(this, linea):

        # finditer: encuentra todas las cadenas que coinciden con la expresión regular en la cadena y devuélvelas como un iterador
        # El string es examinada de izquierda a derecha, y las coincidencias son retornadas en el orden en que se encuentran
        for match in re.finditer(this.patterns, linea):
            # Caracteres que coinciden con toda la expresión, la función yield es similar a return, devuelve un generador,
            # Un generador se comporta parecido a una lista, en el sentido que puede ser recorrida con un iterador - la diferencia es que los valores
            # no están almacenados en una colección, sino que se generan "on the fly".
            yield (match.lastgroup, match.group())

            s = match.start()
            e = match.end()
            print('El símbolo "%s" aparece entre %d:%d' % (linea[s:e], s, e))


# En esta clase Tokenizer se hará la creación de la tabla de tokens, su ID y el lexema que lo genera, además de lla respectiva ubicación.

class TOKENIZER(NamedTuple):
    # Se especifican los campos que tendrá la Tupla correspondiente a la representación visual de la información.

    TOKEN: str
    lEXEMA: str
    line: int
    column: int


# Método tokenize, en el cual se definen detalladamente los tokens y el respectivo proceso para su análisis.
def tokenize(code):
    # Lista de palabras reservadas.
    keywords = ['and', 'for', 'if', 'else', 'is', 'break', 'try', 'not',
                'import', 'continue', 'return', 'from', 'while', 'print',
                'def', 'in', 'or']
    # Lista de tokens usando expresiones regulares.
    token_specification = [
        ('Numero', r'\d+(\.\d*)?'),  # número entero o decimal
        ('ASSIGN', r'='),
        ('Compare', r':='),
        ('SeparadorComa', r','),  # finalización de estancia
        ('OperadorDiv', r'/'),
        ('OperadorMul', r'\*'),
        ('ID', r'[A-Za-z]+'),
        # Identificadores, que es cualquier string que no pertenezca a la lista de palabras reservadas.
        ('OPSUM', r'[+]'),
        ('OPRES', r'[\-]'),
        ('ParenIzq', r'[(]'),
        ('ParenDer', r'[)]'),
        ('LlaveIzq', r'[{]'),
        ('LlaveDer', r'[}]'),
        ('mayorQue', r'[>]'),
        ('menorQue', r'[<]'),
        ('NEWLINE', r'\n'),  # Finalización de lineas
        ('SKIP', r'[ \t]+'),  # espacios y tabs
        ('MISMATCH', r'.'),  # Cualquier otro caracter
    ]
    # Instacia de la librería PrettyTable para la organización de la información agradable a la vista
    x = PrettyTable()
    x.field_names = ["TOKEN/ID TOKEN", "LEXEMA", "LINEA", "COLUMNA"]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0

    # Ciclo para comparar y separar tokens caracter por caracter especificando su ID y su nombre (kind en este caso)
    # y utilizando el método finditer de regex para las expresiones regulares. En el caso de que el kind sea un mismatch,
    # se mostrará el error.

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

        # Se organiza todo para luego juntarse, con el propósito de mostrarlo de forma organizada con ayuda de la librería
        # PrettyTable.

        yield TOKENIZER(kind, value, line_num, column)
        x.add_row([kind, value, line_num, column])

    print("")
    print("          Organización en prettyTable ")
    print("")
    print("--------------------PrettyTable-------------------")
    print(x)


class ExprAritmetica(object):

    # Se crea __init__ para almacenar las expresiones aritméticas necesarias para el análisis, además de inicializar los
    # operadores aritméticos con los cuales se van a trabajar. En este caso los arreglos de expresionAritmetica,
    # expresionesAritmeticas y posicionOpAritmetica se inicializan sin un valor específico ya que posteriormente
    # se irán llenando con valores de acuerdo a la función a la que fueron asignados dentro del código.

    def __init__(this, source_code):

        this.source_code = source_code

        this.operadorAritmetico = ['+', '-', '*', '/', '^', '%', '(', ')']
        this.expresionAritmetica = []
        this.expresionesAritmeticas = []
        this.posicionOpAritmetica = []

    # Función que guarda operaciones aritméticas, verifica caracter por caracter si es un operador aritmético
    # o un número, si lo es se añade al arreglo de expresiones aritméticas, se llama varias veces en la función de
    # analizarExprAritmeticas, en caso de que se reciba un caracter o un string que se salga de las condiciones,
    # convierte la expresión analizada en ese paso un string, luego se añade al arreglo de expresionesAritméticas,
    # si tiene tamaño 1 no se considera expresión aritmética y no se añade el arreglo de expresionesAritméticas.
    # Para finalizar, se utiliza .clear() para que la próxima vez que busque una operación aritmética, se encuentre
    # limpio el arreglo.

    def buscarOperacionAritmetica(this, palabra, fila):

        if palabra in this.operadorAritmetico or palabra.isnumeric():
            this.expresionAritmetica.append(palabra)
        else:
            exp = "".join(this.expresionAritmetica)
            if exp and len(this.expresionAritmetica) > 1:
                this.expresionesAritmeticas.append(exp)
                this.posicionOpAritmetica.append(fila)

            this.expresionAritmetica.clear()

    # Esta función comprueba si las expresiones aritméticas con o sin paréntesis son correctas. Se encarga mediante un
    # ciclo y la implementación de dos contadores (caracter y expresión) para analizar si existen por lo menos dos números
    # y un operador, con esto se podría considerar que es una posible expresión aritmética. Si no se cumplen las
    # condiciones anteriormente mencionadas, se saca del arreglo de expresiones aritméticas.

    def comprobarExpAritmetica(this):

        expresion = ""
        cont = 0
        expresionesAritmeticasAux = this.expresionesAritmeticas.copy()
        for expr in expresionesAritmeticasAux:
            contCaracter = 0
            contExpresion = 0
            for char in expr:
                cont += 1
                if char in this.operadorAritmetico or cont == len(expr):
                    contCaracter += 1
                    if cont == len(expr) or expresion.isnumeric():
                        contExpresion += 1

                    expresion = ""
                else:
                    expresion += char
            if contCaracter == 0 or contExpresion <= 1:
                this.posicionOpAritmetica.pop(this.expresionesAritmeticas.index(expr))
                this.expresionesAritmeticas.remove(expr)

    # Recorre el arreglo donde se almacenan las expresiones aritméticas posición por posición en un ciclo,
    # que tiene como propósito imprimir la tabla para mostrar las posibles expresiones aritméticas analizadas,
    # y su ubicación dentro del código fuente.

    def imprimirExprAritmeticas(this):

        tablaExprArit = PrettyTable()
        tablaExprArit.field_names = ["Expresión Aritmética", "Fila"]

        i = 0
        while i < len(this.expresionesAritmeticas):
            tablaExprArit.add_row([this.expresionesAritmeticas[i], this.posicionOpAritmetica[i]])
            tablaExprArit.add_row(["------------", "------------"])
            i = i + 1

        print(tablaExprArit)

    def gramaticaExprArit(self):
        layout2 = [[sg.Text('Digite el número de la expresión para revisar sintaxis', size=(40, 1)), sg.InputText()],
                   [sg.Button('¡Analizar!')]]
        window2 = sg.Window('Sintaxis', layout2)
        event, values = window2.read()
        window2.close()

        opcionElegida = int(values[0])
        self.source = self.expresionesAritmeticas[opcionElegida - 1]
        g = grm(self.source)
        g.iniciarAnalisis()

    # Con el source_code (contenido del archivo a analizar sus expresiones aritméticas), lo divide por líneas, luego lo
    # lee caracter por caracter y verifica si el valor analizado es un número o un paréntesis. Si lo es, se llama a la
    # función buscarOperacionAritmetica que hace el análisis correspondiente. Luego, se llama la función que comprueba
    # si una expresión aritmética está bien escrita o no. Por último, se hace una revision de las
    # operaciones aritmeticas, utiizando nuevamente la funcion buscarOperacionAritmetica y despues  se llama de nuevo la
    # función comprobarExpAritmética para hacer un último chequeo. Se imprimen los resultados
    # y se llama en el main el método.

    def analizarExprAritmeticas(this):

        expr = ""
        fila = 0

        source_code = this.source_code.split()

        for line in source_code:
            fila += 1
            columna = 0
            for char in line:

                columna += 1

                if char in this.operadorAritmetico or char.isnumeric():

                    if expr.isnumeric():
                        this.buscarOperacionAritmetica(expr, fila)

                    this.buscarOperacionAritmetica(char, fila)
                    expr = ""

                else:
                    expr = expr + char

            this.buscarOperacionAritmetica("", fila)
            this.comprobarExpAritmetica()

        this.imprimirExprAritmeticas()
        this.buscarOperacionAritmetica("", fila)
        this.comprobarExpAritmetica()


# Se crea la clase gramática, la cual se encarga de verificar la sintaxis de las posibles expresiones aritméticas,
# mediante la implementación de la gramática libre de contexto correspondiente, en caso de que la expresión
# aritmética sea rechazada se mostrará la razón del error y su ubicación dentro del código. Además se añade un
#Variables necesarias para revisión de grámatica: String source, Int posición, Int aux,boolean mal (Para interanctuar con el estado de la revisión), Token entrada que es la posición inicial de source
#Variables de puntos de intervención: String pos, String alm, String pre, String auxPre, Lista pila, Lista pilaAyuda

class grm:

    def __init__(self,source):
        self.source = source
        self.posicion = 0
        self.aux = 0
        self.tokenEntrada = source[0]
        self.mal = False
        self.pos = ""
        self.alm = ""
        self.pre = ""
        self.auxPre = ""
        self.pila = []
        self.pilaAyuda = []

    def error(self):
        messagebox.showinfo(message="Hay errores en su expresión : " + self.source + "\nNo se acepta la expresión ", title="Error de sintaxis")

    # Funciones exclusivas de la Gramática Libre de Contexto, que se encargar de verificar la sintaxis correspondiente
    # de cada posible expresión aritmética que se desee analizar. Se implementó la eliminación de la recursividad a la
    # izquierda para su programación.

    # La función expresión llama recursivamente a la función término y a la función expresión prima

    def expresion(self):
        self.termino()
        self.expresion_prima()
        self.pre += self.alm        #Punto de intervención ( sumamos a pre lo que haya en alm y luego reiniciamos alm)
        self.alm = ""

    # La función expresión prima compara el token de entrada y verifica si es un operador suma o un operador resta,
    # en este caso se dirigiría a la función hacerMatch con ese token de entrada, ya que los operadores suma o resta
    # son tokens terminales. Por último, se llama recursivamente a la función término y a la función expresión prima.
    # En caso de que no se encuentre un operador suma o un operador resta, no se hace nada (EPSILON).

    def expresion_prima(self):
        if self.tokenEntrada == "+":
           self.pre += "+ " + self.alm          #Punto de interveción (Se encarga de poner operador suma/resta delante del alm que se tenga y almacenar en pre)
           self.alm = ""
           self.hacerMatch(self.tokenEntrada)

           self.termino()
           self.pos += "+"    #Punto de intervención (Añade el operador al String pos)
           self.expresion_prima()

        elif self.tokenEntrada == "-":
            self.pre += "- " + self.alm      #Punto de intervención
            self.alm = ""
            self.hacerMatch(self.tokenEntrada)

            self.termino()
            self.pos += "-"    #Punto de intervención (Añade el operador al String pos)
            self.expresion_prima()

        else:
            return ''

    # La función termino llama recursivamente a la función factor y a la función término prima

    def termino(self):
        self.factor()
        self.termino_prima()

    # La función término prima compara el token de entrada y verifica si es un operador multiplicación o un operador
    # división, en este caso se dirigiría a la función hacerMatch con ese token de entrada, ya que los operadores
    # multiplicación o división son tokens terminales. Por último, se llama recursivamente a la función término y a
    # la función expresión prima. En caso de que no se encuentre un operador multiplicación o un operador división,
    # no se hace nada (EPSILON).
    #De esta misma forma, se tienen varios puntos de intervención correspondientes a la traducción a prefijo y postfijo
    #de la expresión.

    def termino_prima(self):
        self.auxPre = self.alm
        if self.tokenEntrada == "*":
            self.alm = "* " + self.auxPre   #Punto de interveción (Se encarga de poner operador multiplicación/división delante del alm que se tenga)
            self.hacerMatch(self.tokenEntrada)

            self.factor()
            self.pos += "*"    #Punto de intervención (Añade el operador al String pos)
            self.termino_prima()

        elif self.tokenEntrada == "/":
            self.alm = "/" + self.auxPre  #Punto de intervención (Se encarga de poner operador delante del alm que se tenga)
            self.hacerMatch(self.tokenEntrada)

            self.factor()
            self.pos += "/"    #Punto de intervención(Añade el operador al String pos)
            self.termino_prima()

        else:
            return ''

    # La función factor primero analiza si el token de entrada es un paréntesis abierto, en este caso al ser un token
    # terminal se llama a la función hacerMatch y se llama recursivamente a la función expresión, luego de esto se
    # verifica que el token de entrada sea ahora un paréntesis cerrado, si lo es, se llama a la función hacerMatch ya
    # que es un token terminal. Si no hay un paréntesis cerrado, se imprime el error de sintaxis correspondiente.
    # Si por otro caso el token de entrada es un dígito, se llama recursivamente a la función número, si es una
    # letra minúscula, se llama recursivamente a la función variable.
    #Además, para realizar la traducción a postfijo y prefijo, se utilizan la variable pre, alm y una pila,siendo
    # utilizadas al principio de la función para almacenar la información de pre en la pila y posteriormente, cuando se
    #verifica la buena disposición, también se revisa que la pila se encuentre vacia y si no lo está,
    #Se crea una variable axial en la cual almacenamos la información contenida en pre y alm para posteriormente
    #hacer que almacenamiento sea igual a .pop(), es decir, el último elemento de la pila y almacenamiento sea igual a axial
    #De esta forma se obtiene la forma de prefijo requerida.

    def factor(self):
        if self.tokenEntrada == "(":
            self.hacerMatch(self.tokenEntrada)
            self.pre += self.alm
            self.pila.append(self.pre)
            self.pre = ""
            self.alm = ""

            if self.tokenEntrada != ")":
                self.expresion()
                if self.tokenEntrada == ")":
                    self.hacerMatch(")")

                else:
                    messagebox.showinfo(
                        message="¡Error de sintaxis! \nRevisar que '(' o ')' estén correctamente indicados",
                        title="Error sintaxis")
                    self.mal = True

            if not bool(self.pilaAyuda):
                self.axial = self.pre + self.alm
                self.pre = self.pila.pop()
                self.alm = self.axial

        elif self.tokenEntrada.isdigit():
            self.numero()

        elif self.tokenEntrada.islower():
            self.variable()

    # La función número llama recursivamente a la función dígito y a la función número prima

    def numero (self):
        self.digito()
        self.numero_prima()
        self.pos+=" "      #Punto de intervención
        self.alm+=" "      #Punto de intervención

    # La función número prima compara el token de entrada y verifica si es un dígito, en este caso se dirigiría
    # a la función hacerMatch con ese token de entrada, ya que un dígito es un token terminal. Por último,
    # se llama recursivamente a la función dígito y a la función número prima. En caso de que no se encuentre
    # un dígito como token de entrada, no se hace nada (EPSILON).

    def numero_prima(self):
        if self.tokenEntrada.isdigit():
            self.digito()
            self.numero_prima()

    # La función variable llama recursivamente a la función caracter y a la función variable prima

    def variable(self):
        self.caracter()
        self.variable_Prima()

    # La función variable prima verifica si el token de entrada es una letra minúscula, si lo es, se llama
    # recursivamente a la función caracter y a la función variable prima.

    def variable_Prima(self):
        if self.tokenEntrada.islower():
            self.caracter()
            self.variable_Prima()

    # La función digito verifica si el token de entrada es un dígito, si lo es, se llama a la función hacerMatch
    # ya que es un token terminal y se añade el token de entrada a la variable pos y alm.

    def digito(self):
        if self.tokenEntrada.isdigit():
            self.pos += self.tokenEntrada    #Punto de intervención
            self.alm += self.tokenEntrada    #Punto de intervención
            self.hacerMatch(self.tokenEntrada)

    # La función caracter verifica si el token de entrada es una letra minúscula, si lo es, se llama a la función
    # hacerMatch ya que es un token terminal.

    def caracter(self):
        if self.tokenEntrada.islower():
            self.hacerMatch(self.tokenEntrada)

    # La función siguiente token primero incrementa la posición en la que se encuentra el token a analizar,
    # posteriormente verifica si el tamaño del source es mayor al tamaño de la posición en la que se encuentra,
    # si lo es, retorna la posición actual para ser analizada. Si no, retorna EPSILON.

    def siguienteToken(self):
        self.posicion = self.posicion + 1
        if len(self.source) > self.posicion:
            return self.source[self.posicion]
        else:
            return ''

    # La función hacerMatch analiza el token de entrada, teniendo en cuenta características básicas de las
    # expresiones aritméticas, llamando recursivamente a la función siguienteToken para moverse recursivamente por
    # el vector o string.

    # Si la expresión aritmética finaliza con un operador, se mostrará un mensaje de error correspondiente con la
    # ubicación del mismo.

    # Si la expresión aritmética tiene dos o más operadores consecutivos, se mostrará un mensaje de error, puesto
    # que luego de un operador, debe seguir un número, letra o paréntesis.

    def hacerMatch(self, t):
        if t == self.tokenEntrada:
            print("Analizando: " + self.tokenEntrada)

            if self.tokenEntrada == "+":

                self.suffix = "+"
                if self.source.endswith(self.suffix):
                    messagebox.showinfo(
                        message="Error en posición:" + str(
                            len(self.source)) + "\nLa expresión no puede acabar con operadores , agregue operando",
                        title="Error sintaxis")
                    self.mal = True

                elif self.source[self.posicion + 1] == "/" or self.source[self.posicion + 1] == "*" or self.source[
                    self.posicion + 1] == "+" or self.source[self.posicion + 1] == "-":
                    messagebox.showinfo(
                        message="Error en posición: " + str(
                            self.posicion + 1) + "\nDebe haber dígito después de operador",
                        title="Error sintaxis")
                    print("Error en posición: " + str(self.posicion + 1) + "\nDebe haber dígito después de operador")
                    self.mal = True

            if self.tokenEntrada == "-":
                self.suffix2 = "-"
                if self.source.endswith(self.suffix2):
                    messagebox.showinfo(
                        message="Error en posición:" + str(
                            len(self.source)) + "\nLa expresión no puede acabar con operadores , agregue operando",
                        title="Error sintaxis")
                    print("Error en posición:" + str(
                        len(self.source)) + "\nLa expresión no puede acabar con operadores , agregue operador")
                    self.mal = True

                elif self.source[self.posicion + 1] == "/" or self.source[self.posicion + 1] == "*" or self.source[
                    self.posicion + 1] == "+" or self.source[self.posicion + 1] == "-":
                    messagebox.showinfo(
                        message="Error en posición: " + str(
                            self.posicion + 1) + "\nDebe haber dígito después de operador",
                        title="Error sintaxis")
                    self.mal = True

            if self.tokenEntrada == "/":
                self.suffix2 = "/"
                if self.source.endswith(self.suffix2):
                    messagebox.showinfo(
                        message="Error en posición:" + str(
                            len(self.source)) + "\nLa expresión no puede acabar con operadores , agregue operando",
                        title="Error sintaxis")
                    self.mal = True

                elif self.source[self.posicion + 1] == "/" or self.source[self.posicion + 1] == "*" or self.source[
                    self.posicion + 1] == "+" or self.source[self.posicion + 1] == "-":

                    messagebox.showinfo(
                        message="Error en posición: " + str(
                            self.posicion + 1) + "\nDebe haber dígito después de operador",
                        title="Error sintaxis")
                    self.mal = True

            if self.tokenEntrada == "*":
                self.suffix2 = "*"
                if self.source.endswith(self.suffix2):
                    messagebox.showinfo(
                        message="Error en posición:" + str(
                            len(self.source)) + "\nLa expresión no puede acabar con operadores , agregue operando",
                        title="Error sintaxis")
                    self.mal = True

                elif self.source[self.posicion + 1] == "/" or self.source[self.posicion + 1] == "*" or self.source[
                    self.posicion + 1] == "+" or self.source[self.posicion + 1] == "-":
                    messagebox.showinfo(
                        message="Error en posición: " + str(
                            self.posicion + 1) + "\nDebe haber dígito después de operador",
                        title="Error sintaxis")
                    self.mal = True

                self.tokenEntrada = self.siguienteToken()

            else:
                self.tokenEntrada = self.siguienteToken()

    # La función iniciarAnálisis es con la cual se inicializa el análisis de una expresión, teniendo como condición
    # que la posición analizada siempre sea menor al tamaño de la posible expresión aritmética. Se llama
    # la función expresión, para comenzar la validación mediante la GLC. Si en ningún momento se activa la
    # bandera booleana llamada rejected, encargada de cambiar su valor lógico a true en caso de que haya error,
    # significa que la expreisón aritmética fue validada satisfactoriamente, y se mostrará el mensaje por pantalla.
    # En caso contrario, se mostrará un mensaje de que no fue aceptada.

    def iniciarAnalisis(self):
        self.expresion()
        while self.posicion < len(self.source):
            self.tokenEntrada = self.siguienteToken()
            self.expresion()
        if self.mal == False:
            messagebox.showinfo(message="Se acepta la expresión: " + self.source, title="Sintaxis correcta")
            messagebox.showinfo(message="Traducción a Postfijo: " + self.pos, title="Notación Postfija")
            messagebox.showinfo(message="Traducción a Prefijo: " + self.pre, title="Notación Prefija")

        else:
            self.error()

#Función con la cual se pide un archivo al usuario y se almacena la ruta seleccionada para luego trabajar
#con la información del mismo.

def obtenerArchivo():
    archivo = filedialog.askopenfilename(initialdir="C:/",
                                         title="Elegir archivo .py",
                                         filetypes=(("text files", "*.py"),
                                                    ("all files", "*.*")))
    return (archivo)

#Creación de interfaz gráfica para la interacción con el usuario de una manera más amigable.
#La variable Layout contiene una lista de listas en donde cada una tiene atributos como texto, botones, entre otros
#y a su vez, características como el tamaño y la justificación de los mismos.

sg.theme('SandyBeach')
layout = [[sg.Text('Seleccione Un Archivo',size=(50,1),justification='center')],
          [sg.Button('Elegir Archivo',size=(30,1))],
          [sg.Button('Ejecutar analizador lexicográfico',size=(30,1))],

          [sg.Button('Presentar Tabla de Tokens',size=(30,1))],
          [sg.Button('Analizar expresiones aritmética',size=(30,1))],
          [sg.Button('Revisar Sintaxis',size=(30,1))],
          [sg.Button('salir',size=(30,1))]]

# Se crea la ventana, enfatizando en algunas características de visualización importantes.

window = sg.Window('Compilador', layout,margins=(20,20),size=(350,250),element_justification='c')

# La clase principal ejecuta la interfaz gráfica, que permite un mejor manejo de las diferentes opciones
# a la hora de analizar un archivo, mediante unos botones que cumplen una función determinada, especificada
# en el menú. Gracias a la librería PySimpleGUI, esto se hace de manera interactiva.

def principal():

    file = ""
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'salir':
            break

        if event == sg.WIN_CLOSED or event == 'Elegir Archivo':
            file = obtenerArchivo()
            messagebox.showinfo(message="Ha escogido el archivo exitosamente", title="Archivo")

        if event == 'Ejecutar analizador lexicográfico':
            Analex = Analizador()

            # Leer las lineas del archivo con función read_file
            lineas = Analex.read_file(file)
            # Utilización de ciclo for para llamar la función run que es la que nos genera la tabla final.

            for linea in lineas:
                Analex.run(linea, True)

                Analex.lineno += 1

        if event == 'Presentar Tabla de Tokens':
            print("Los tokens de su archivo son: ")
            print(" ")
            print("---------------TOKENS-------------")

            # Se abre el archivo que contiene el código y posteriormente se lee, para realizar una depuración
            # de este token por token, gracias al ciclo que los va imprimiendo línea por línea.

            archivo = open(file, 'r')
            linea = archivo.read()

            for token in tokenize(linea):
                print(token)

        if event == 'Analizar expresiones aritmética':
            print("Las expresiones aritméticas son : ")
            print("")
            print("--------------Expresiones aritméticas---------")

            # Abre el archivo y lo lee en la clase de ExprAritmetica, la cual llevará el código fuente a la función
            # AnalizarExprAritmeticas, que hará el proceso de buscar las posibles expresiones aritméticas dentro
            # del código en el archivo de prueba, y posteriormente imprimirá esas posibles expresiones aritméticas
            # en una tabla organizada gracias a la implementación de la librería PrettyTable.

            with open(file, 'r') as file2:
                content = file2.read()

                anaArt = ExprAritmetica(content)
                anaArt.analizarExprAritmeticas()

        if event == 'Revisar Sintaxis':
            # Ya con las posibles expresiones aritméticas almacenadas en un arreglo, se llama a la función
            # gramaticaExprArit, la cual llamará a la clase gramática, que tiene implementada la GLC
            # (gramática libre de contexto, que ya tiene eliminada recursividad a la izquierda) para posteriormente
            # hacer una validación de sintáxis de la expresión aritmética, por último se mostrará un mensaje que
            # muestre si la expresión es aceptada o es rechazada, en este último caso, se especificará la razón
            # mediante el tipo de error que se cometió dentro del código y su ubicación.

            with open(file, 'r') as file2:
                content = file2.read()

                anaArt = ExprAritmetica(content)
                anaArt.analizarExprAritmeticas()
                anaArt.gramaticaExprArit()

principal()