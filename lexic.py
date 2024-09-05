import re
from simple_language import Token, TokenType

class SimpleLexer:
    def __init__(self):
        self.tokens = []
        self.symbol_table = {}
        self.current_line = 1
        self.current_column = 0
        self.last_line_number = 0
    
    def open_txt_file(self, simple_file):
        try:
            with open(simple_file, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return f"Arquivo não encontrado."
        except Exception as e:
            return f"Erro ao ler o arquivo."

    def process_txt(self, simple_file):
        simple_file_content = self.open_txt_file(simple_file)
        simple_file_content = simple_file_content.split('\n')
        
        for line in simple_file_content:
            if line.strip() == '':
                self.current_line += 1
                continue
            
            tokens = line.split()
            if len(tokens) == 0:
                self.current_line += 1
                continue

            if not tokens[0].isdigit() or int(tokens[0]) <= 0:
                raise ValueError(f"Erro: linha {self.current_line} não começa com um número de linha válido.")
            
            line_number = int(tokens[0])
            self.tokens.append(Token(TokenType.LINENUMBER, line_number, self.current_line, 0))

            rest_of_line = ' '.join(tokens[1:])
            self.tokenize(rest_of_line)

            self.current_line += 1
            self.current_column = 0 

    def tokenize(self, line):
        token_specification = [
            ('GE', r'>='),           
            ('LE', r'<='),           
            ('NE', r'!='),          
            ('EQ', r'=='),          
            ('GT', r'>'),           
            ('LT', r'<'),            
            ('ASSIGNMENT', r'='),  
            ('ADD', r'\+'),         
            ('SUBTRACT', r'-'),     
            ('MULTIPLY', r'\*'),    
            ('DIVIDE', r'/'),  
            ('MODULO', r'%'),   

            ('REM', r'\brem\b'),            
            ('INPUT', r'\binput\b'),
            ('LET', r'\blet\b'),
            ('PRINT', r'\bprint\b'),
            ('GOTO', r'\bgoto\b'),
            ('IF', r'\bif\b'),
            ('END', r'\bend\b'),  
                        
            ('INVALID_UPPERCASE', r'\b[A-Z]\b'),  
            ('VARIABLE', r'\b[a-z]\b'),  
            ('INVALID_VARIABLE', r'\b[a-zA-Z]{2,}\b'), 
            ('INTEGER', r'\b\d+\b'),
            ('SKIP', r'[ \t]+'),
        ]
        
        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        line_iter = re.finditer(token_regex, line)
        
        for match in line_iter:
            kind = match.lastgroup
            lexeme = match.group(kind)
            column = match.start()
            
            if kind == 'SKIP':
                continue
            
            elif kind == 'REM':
                self.add_token(TokenType.REM, lexeme, column)
                return
            
            elif kind == 'MISMATCH':
                self.add_token(TokenType.ERROR, lexeme, column)
            else:
                token_type = getattr(TokenType, kind)
                self.add_token(token_type, lexeme, column)

    def add_token(self, token_type, lexeme, column):
        self.tokens.append(Token(token_type, lexeme, self.current_line, column))
