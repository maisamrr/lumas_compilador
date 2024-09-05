import re

token_index = 0
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

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.symbol_table = {}
        self.current_line = 1
        self.current_column = 0
        self.last_line_number = 0

    def add_token(self, token_type, lexeme):
        address = self.add_to_symbol_table(lexeme)
        token = Token(token_type, address, self.current_line, self.current_column)
        self.tokens.append(token)

    def add_to_symbol_table(self, lexeme):
        if lexeme not in self.symbol_table:
            self.symbol_table[lexeme] = len(self.symbol_table) + 1
        return self.symbol_table[lexeme]

    def tokenize(self, line):
        line = line.strip()
        
        # Verificar se o número da linha é válido (só no início da linha)
        line_number_match = re.match(r'^\d+', line)
        if not line_number_match:
            raise SyntaxError("Erro: A linha não começa com um número de linha.")
        
        line_number = int(line_number_match.group(0))
        if line_number <= self.last_line_number:
            raise SyntaxError(f"Erro de numeração da linha: {line_number}. Numeração de linha repetida ou fora de ordem.")
        self.last_line_number = line_number
        self.add_token(TokenType.LINENUMBER, str(line_number))

        line = line[len(str(line_number)):].strip()
        
        token_specification = [
            ('LF', r'\n', TokenType.LF),           
            ('GE', r'>=', TokenType.GE),           
            ('LE', r'<=', TokenType.LE),           
            ('NE', r'!=', TokenType.NE),          
            ('EQ', r'==', TokenType.EQ),          
            ('GT', r'>', TokenType.GT),           
            ('LT', r'<', TokenType.LT),            
            ('ASSIGNMENT', r'=', TokenType.ASSIGNMENT),  

            ('ADD', r'\+', TokenType.ADD),         
            ('SUBTRACT', r'-', TokenType.SUBTRACT), 
            ('MULTIPLY', r'\*', TokenType.MULTIPLY), 
            ('DIVIDE', r'/', TokenType.DIVIDE),  
            ('MODULO', r'%', TokenType.MODULO),   

            ('REM', r'\brem\b', TokenType.REM),            
            ('INPUT', r'\binput\b', TokenType.INPUT),
            ('LET', r'\blet\b', TokenType.LET),
            ('PRINT', r'\bprint\b', TokenType.PRINT),
            ('GOTO', r'\bgoto\b', TokenType.GOTO),
            ('IF', r'\bif\b', TokenType.IF),
            ('END', r'\bend\b', TokenType.END),

            # sequência de letras inválida
            ('INVALID_VAR', r'[a-z]{2,}', TokenType.ERROR),  
            
            # variável só pode ser letra única isolada
            ('VARIABLE', r'\b[a-z]\b', TokenType.VARIABLE),  
            ('INTEGER', r'\b\d+\b', TokenType.INTEGER),
        ]
        
        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        
        iterator = re.finditer(token_regex, line, re.MULTILINE)
        for match in iterator:
            kind = match.lastgroup
            lexeme = match.group(kind)
            self.current_column = match.start() - self.code.rfind('\n', 0, match.start())

            # verifica maiúsculas no lexema
            if any(char.isupper() for char in lexeme):
                kind = 'MISMATCH'

            # comentários
            if kind == 'REM':
                self.add_token(TokenType.REM, lexeme)
                while True:
                    next_match = next(iterator, None)
                    if next_match is None or next_match.lastgroup == 'LF':
                        break
                self.current_line += 1
                self.current_column = 0
                continue

            if kind == 'LF':
                self.current_line += 1
                self.current_column = 0
                continue
                
            if kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                self.add_token(TokenType.ERROR, lexeme)
            else:
                token_type = next(pair[2] for pair in token_specification if pair[0] == kind)
                self.add_token(token_type, lexeme)

        return self.tokens

def get_next_token():
    global token_index
    if token_index < len(tokens):
        token = tokens[token_index]
        token_index += 1
        return token
    else:
        raise SyntaxError("Fim dos tokens inesperado")

def peek_next_token():
    if token_index < len(tokens):
        return tokens[token_index]
    else:
        raise SyntaxError("Fim dos tokens inesperado")
    
def parse_line_number():
    global last_line_number
    token = get_next_token()
    if token.token_type != TokenType.LINENUMBER:
        raise SyntaxError(f"Erro de sintaxe: Esperava-se um número de linha na linha {token.line}, coluna {token.column}")
    line_number = int(token.symbol_address)
    if line_number <= last_line_number:
        raise SyntaxError(f"Erro de sintaxe: Número de linha {line_number} fora de ordem")
    last_line_number = line_number

# parse do input
def parse_input():
    token = get_next_token()
    if token.token_type != TokenType.VARIABLE:
        raise SyntaxError(f"Erro de sintaxe: Esperava-se uma variável após 'input' na linha {token.line}, coluna {token.column}")

# parse do let
def parse_assignment():
    token = get_next_token()
    if token.token_type != TokenType.VARIABLE:
        raise SyntaxError(f"Erro de sintaxe: Esperava-se uma variável após 'let' na linha {token.line}, coluna {token.column}")

    token = get_next_token()
    if token.token_type != TokenType.ASSIGNMENT:
        raise SyntaxError(f"Erro de sintaxe: Esperava-se '=' após a variável na linha {token.line}, coluna {token.column}")

    parse_expression()

def parse_print():
    token = get_next_token()
    if token.token_type != TokenType.VARIABLE:
        raise SyntaxError(f"Erro de sintaxe: Esperava-se uma variável após 'print' na linha {token.line}, coluna {token.column}")

def parse_goto():
    token = get_next_token()
    if token.token_type != TokenType.INTEGER:
        raise SyntaxError(f"Erro de sintaxe: Esperava-se um número inteiro após 'goto' na linha {token.line}, coluna {token.column}")

def parse_if_statement():
    parse_condition()

    token = get_next_token()
    if token.token_type != TokenType.GOTO:
        raise SyntaxError(f"Erro de sintaxe: Esperava-se 'goto' após a condição na linha {token.line}, coluna {token.column}")

    token = get_next_token()
    if token.token_type != TokenType.INTEGER:
        raise SyntaxError(f"Erro de sintaxe: Esperava-se um número inteiro após 'goto' na linha {token.line}, coluna {token.column}")

# parse de condicionais
def parse_condition():
    parse_expression()

    token = get_next_token()
    if token.token_type not in (TokenType.EQ, TokenType.NE, TokenType.GT, TokenType.LT, TokenType.GE, TokenType.LE):
        raise SyntaxError(f"Erro de sintaxe: Esperava-se um operador relacional na linha {token.line}, coluna {token.column}")

    parse_expression()

def parse_end():
    pass

# parse de + e -
def parse_expression():
    parse_term()

    token = peek_next_token()
    while token.token_type in (TokenType.ADD, TokenType.SUBTRACT):
        get_next_token()
        parse_term()
        token = peek_next_token()

# parse de *, / e %
def parse_term():
    parse_factor()

    token = peek_next_token() 
    while token.token_type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
        get_next_token() 
        parse_factor()  
        token = peek_next_token() 

# parse de variáveis e inteiros
def parse_factor():
    token = get_next_token()

    if token.token_type == TokenType.VARIABLE:
        return
    elif token.token_type == TokenType.INTEGER:
        return
    else:
        raise SyntaxError(f"Erro de sintaxe: Esperava-se uma variável ou um número na linha {token.line}, coluna {token.column}")
    
# parse de palavras reservadas - rem, input, let, print, goto, if, end
def parse_statement():
    token = peek_next_token()
    if token.token_type == TokenType.LINENUMBER:
        parse_line_number()
        token = get_next_token() 
    else:
        raise SyntaxError(f"Erro de sintaxe: Esperava-se um número de linha na linha {token.line}, coluna {token.column}")

    if token.token_type == TokenType.REM:
        pass 
    elif token.token_type == TokenType.INPUT:
        parse_input()
    elif token.token_type == TokenType.LET:
        parse_assignment()
    elif token.token_type == TokenType.PRINT:
        parse_print()
    elif token.token_type == TokenType.GOTO:
        parse_goto() 
    elif token.token_type == TokenType.IF:
        parse_if_statement()
    elif token.token_type == TokenType.END:
        parse_end()
    else:
        raise SyntaxError(f"Erro de sintaxe na linha {token.line}, coluna {token.column}")

# Exemplo de uso
code = '''
10 input x
15 if x == 0 goto 45
20 input n
25 if n == 0 goto 45
'''

lexer = Lexer(code)

for line in code.strip().split('\n'):
    lexer.tokenize(line)

# imprime tokens:
# for token in lexer.tokens:
#    print(token)