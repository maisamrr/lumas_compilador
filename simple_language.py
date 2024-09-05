class Token:
    def __init__(self, token_type, symbol_address, line, column):
        self.token_type = token_type
        self.symbol_address = symbol_address
        self.line = line 
        self.column = column 

    def __repr__(self):
        return f"Token({self.token_type}, Addr: {self.symbol_address}, Line: {self.line}, Col: {self.column})"

class TokenType:
    # delimitadores
    LF = 10
    ETF = 3

    # operadores
    ASSIGNMENT = 11

    # operadores aritméticos
    ADD = 21
    SUBTRACT = 22
    MULTIPLY = 23
    DIVIDE = 24
    MODULO = 25

    # operadores relacionais
    EQ = 31    # Igual
    NE = 32    # Diferente
    GT = 33    # Maior que
    LT = 34    # Menor que
    GE = 35    # Maior ou igual
    LE = 36    # Menor ou igual

    # identificadores
    VARIABLE = 41
    
    # constantes númericas inteiras
    INTEGER = 51
    LINENUMBER = 52

    # palavras reservadas
    REM = 61
    INPUT = 62
    LET = 63
    PRINT = 64
    GOTO = 65
    IF = 66
    END = 67
    
    # outros
    ERROR = 99

