import re

# analise lexica

def create_token_pattern(name, pattern):
    return f'(?P<{name}>{pattern})'

def combine_patterns(pattern_dict):
    return '|'.join(create_token_pattern(name, pattern) for name, pattern in pattern_dict.items())

token_patterns = {
    "INTEIRO": r'\d+',
    "ID": r'[A-Za-z_]\w*',
    "LET": r'LET',
    "PRINT": r'PRINT',
    "INPUT": r'INPUT',
    "GOTO": r'GOTO',
    "IF": r'IF',
    "REM": r'REM',
    "END": r'END',
    "ADD": r'\+',
    "MENOS": r'-',
    "VEZES": r'\*',
    "DIVIDIR": r'/',
    "ATRIBUIR": r'=',
    "MENOR": r'<',
    "MAIOR": r'>',
    "MENORIGUAL": r'<=',
    "MAIORIGUAL": r'>=',
    "DIFERENTE": r'!=',
    "IGUAL": r'==',
    "NOVALINHA": r'\n',
    "IGNORAR": r'[ \t]+',
    "NAORECONHECE": r'.'
}

token_regex = combine_patterns(token_patterns)

def tokenize(code):
    tokens_reconhecidos = []
    linha_num = 1
    linha_start = 0
    
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        column = mo.start() - linha_start
        
        if kind == "INTEIRO":
            value = int(value)
        elif kind == "ID" and value in {"LET", "PRINT", "INPUT", "GOTO", "IF", "REM", "END"}:
            kind = value.upper()
        elif kind == "NOVALINHA":
            linha_start = mo.end()
            linha_num += 1
            continue
        elif kind == "IGNORAR":
            continue
        elif kind == "NAORECONHECE":
            raise RuntimeError(f'{value!r} não reconhecido na linha {linha_num}')
        
        tokens_reconhecidos.append((kind, value, linha_num, column))
    
    tokens_reconhecidos.append(("EOF", "", linha_num, column))
    return tokens_reconhecidos

teste = '''
LET X = 10
IF X > 5 GOTO 10
PRINT X + 2
'''

tokens = tokenize(teste)
for token in tokens:
    print(token)

# analise sintatica
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        while self.current_token()[0] != "EOF":
            self.statement()

    def statement(self):
        token_type, token_value, line, column = self.current_token()

        if token_type == "LET":
            self.match("LET")
            self.match("ID")
            self.match("ATRIBUIR")
            self.expression()
        elif token_type == "PRINT":
            self.match("PRINT")
            self.expression()  # Aceitar expressões no PRINT
        elif token_type == "IF":
            self.match("IF")
            self.match("ID")
            self.relational_operator()
            self.match("INTEIRO")
            self.match("GOTO")
            self.match("INTEIRO")
        elif token_type == "END":
            self.match("END")
        else:
            self.error(f"Comando inesperado {token_value!r} na linha {line}, coluna {column}")

    def expression(self):
        self.term()  # Lida com o primeiro termo
        while self.current_token()[0] in {"ADD", "MENOS"}:  # Lida com + e -
            self.match(self.current_token()[0])
            self.term()  # Lida com o próximo termo

    def term(self):
        self.factor()  # Lida com o fator inicial
        while self.current_token()[0] in {"VEZES", "DIVIDIR"}:  # Lida com * e /
            self.match(self.current_token()[0])
            self.factor()  # Lida com o próximo fator

    def factor(self):
        token_type, token_value, line, column = self.current_token()
        if token_type in {"INTEIRO", "ID"}:  # Fator pode ser um número ou uma variável
            self.match(token_type)
        else:
            self.error(f"Fator esperado, mas encontrado {token_type} ({token_value!r}) na linha {line}, coluna {column}")

    def relational_operator(self):
        if self.current_token()[0] in {"MENOR", "MAIOR", "MENORIGUAL", "MAIORIGUAL", "DIFERENTE", "IGUAL"}:
            self.match(self.current_token()[0])
        else:
            self.error(f"Operador relacional esperado na linha {self.current_token()[2]}, coluna {self.current_token()[3]}")

    def match(self, expected_type):
        token_type, token_value, line, column = self.current_token()

        if token_type == expected_type:
            self.pos += 1
        else:
            self.error(f"Esperado {expected_type}, mas encontrado {token_type} ({token_value!r}) na linha {line}, coluna {column}")

    def current_token(self):
        return self.tokens[self.pos]

    def error(self, message):
        raise SyntaxError(message)

# Testando o parser com os tokens gerados
parser = Parser(tokens)
parser.parse()
print("Análise sintática concluída com sucesso.")