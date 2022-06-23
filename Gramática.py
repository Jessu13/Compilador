from tkinter import messagebox

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
        self.aux = ""
        self.pila = []
        self.pilaAyuda =[]

    def error(self):
        messagebox.showinfo(message="Hay errores en su expresión, no se acepta la expresión ", title="Error de sintaxis")

    def expresion(self):
        self.termino()
        self.expresion_prima()
        self.pre += self.alm
        self.alm = ""

    def expresion_prima(self):
        if self.tokenEntrada == "+":
           self.pre += "+ " + self.alm
           self.alm = ""
           self.hacerMatch(self.tokenEntrada)

           self.termino()
           self.pos += "+"
           self.expresion_prima()

        elif self.tokenEntrada == "-":
            self.pre += "- " + self.alm
            self.alm = ""
            self.hacerMatch(self.tokenEntrada)

            self.termino()
            self.pos += "-"
            self.expresion_prima()

        else:
            return ''

    def termino(self):
        self.factor()
        self.termino_prima()

    def termino_prima(self):
        self.aux = self.alm
        if self.tokenEntrada == "*":
            self.alm = "* " + self.aux
            self.hacerMatch(self.tokenEntrada)

            self.factor()
            self.pos += "*"
            self.termino_prima()

        elif self.tokenEntrada == "/":
            self.alm = "/" + self.aux
            self.hacerMatch(self.tokenEntrada)

            self.factor()
            self.pos += "/"
            self.termino_prima()

        else:
            return ''

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
                    messagebox.showinfo(message="¡Error de sintaxis! \nRevisar que '(' o ')' estén correctamente indicados",
                                    title="Error sintaxis")
                    self.mal = True

            if not bool(self.pilaAyuda):
                self.axial = self.pre + self.alm
                self.pre = self.pila.pop();
                self.alm = self.axial;

        elif self.tokenEntrada.isdigit():
            self.numero()

        elif self.tokenEntrada.islower():
            self.variable()

    def numero (self):
        self.digito()
        self.numero_prima()
        self.pos+=" "
        self.alm+=" "

    def numero_prima(self):
        if self.tokenEntrada.isdigit():
            self.digito()
            self.numero_prima()

    def variable(self):
        self.caracter()
        self.variable_Prima()

    def variable_Prima(self):
        if self.tokenEntrada.islower():
            self.caracter()
            self.variable_Prima()

    def digito(self):
        if self.tokenEntrada.isdigit():
            self.pos += self.tokenEntrada
            self.alm += self.tokenEntrada
            print(self.alm)
            self.hacerMatch(self.tokenEntrada)

    def caracter(self):
        if self.tokenEntrada.islower():
            self.hacerMatch(self.tokenEntrada)

    def siguienteToken(self):
        self.posicion = self.posicion + 1
        if len(self.source) > self.posicion:
            return self.source[self.posicion]
        else:
            return ''

    def hacerMatch(self,t):
        if t == self.tokenEntrada:
            print("Analizando: " + self.tokenEntrada)

            if self.tokenEntrada == "+":

                self.suffix = "+"
                if self.source.endswith(self.suffix):
                    messagebox.showinfo(
                        message="Error en posición:" + str(
                            len(self.source)) + "\nLa expresión no puede acabar con operadores , agregue operador",
                        title="Error sintaxis")
                    self.mal = True

                elif self.source[self.posicion+1] == "/" or self.source[self.posicion+1] == "*" or self.source[self.posicion+1] == "+" or self.source[self.posicion+1] == "-":
                    messagebox.showinfo(
                        message="Error en posición: " + str(self.posicion+1)+ "\nDebe haber dígito después de operador",
                        title="Error sintaxis")
                    print("Error en posición: " + str(self.posicion+1)+ "\nDebe haber dígito después de operador")
                    self.mal = True

            if self.tokenEntrada == "-":
                self.suffix2 = "-"
                if self.source.endswith(self.suffix2):
                    messagebox.showinfo(
                        message="Error en posición:" + str(len(self.source)) + "\nLa expresión no puede acabar con operadores , agregue operador",
                        title="Error sintaxis")
                    print("Error en posición:" + str(len(self.source)) + "\nLa expresión no puede acabar con operadores , agregue operador")
                    self.mal = True

                elif self.source[self.posicion+1] == "/" or self.source[self.posicion+1] == "*" or self.source[self.posicion+1] == "+" or self.source[self.posicion+1] == "-":
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
                            len(self.source)) + "\nLa expresión no puede acabar con operadores , agregue operador",
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
                            len(self.source)) + "\nLa expresión no puede acabar con operadores , agregue operador",
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


    def iniciarAnalisis(self):
        self.expresion()
        while self.posicion < len(self.source):
            self.tokenEntrada = self.siguienteToken()
            self.expresion()
        if self.mal == False:
            print(self.source)
            messagebox.showinfo(message="Se acepta la expresión: ", title="Sintaxis correcta")
            messagebox.showinfo(message="Traducción a Postfijo: " + self.pos, title="Notación Postfija")
            messagebox.showinfo(message="Traducción a Prefijo: " + self.pre, title="Notación Prefija")

        else:
            print(self.source)
            self.error()

g = grm(source="6+2*4-1/3")
g.iniciarAnalisis()
