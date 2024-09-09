import re
from simple_language import Token, TokenType

class SimpleLexer:
    def __init__(self):
        self.tokens = []
        self.symbol_table = {}
        self.current_line = 0
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

            line_number_match = re.match(r'^\d+', line)
            if not line_number_match:
                raise ValueError(f"Erro: linha {self.current_line} não começa com um número de linha válido.")
            
            line_number = int(line_number_match.group())
            self.tokens.append(Token(TokenType.LINENUMBER, line_number, self.current_line, 0))

            rest_of_line = line[line_number_match.end():]
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
            
            # Variables and integers
            ('VARIABLE', r'\b[a-z]\b'),  
            ('INTEGER', r'\b\d+\b'),
            
            # Uppercase tokens or any token containing uppercase letters
            ('INVALID_UPPERCASE', r'\b[A-Z]+\b'),  # Match uppercase words like 'GOTO'
            
            # Whitespace and invalid characters
            ('SKIP', r'[ \t]+'),  # Match and skip spaces/tabs
            ('INVALID_CHAR', r'[^\w\s+-/*%=<>!]'),  # Match invalid characters
        ]
        
        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        line_iter = re.finditer(token_regex, line)
        
        for match in line_iter:
            kind = match.lastgroup
            lexeme = match.group(kind)
            start_column = self.current_column
            
            if kind == 'SKIP':
                self.current_column += len(lexeme)
                continue
            
            elif kind == 'REM':
                self.add_token(TokenType.REM, lexeme, start_column)
                return
            
            elif kind == 'INVALID_UPPERCASE':
                self.add_token(TokenType.ERROR, lexeme, start_column)
                raise ValueError(f"Maiúscula inválida '{lexeme}' na linha {self.current_line}, coluna {start_column}")
            
            elif kind == 'INVALID_CHAR':
                self.add_token(TokenType.ERROR, lexeme, start_column)
                raise ValueError(f"Caractere invalido '{lexeme}' na linha {self.current_line}, coluna {start_column}")
            
            else:
                token_type = getattr(TokenType, kind)
                self.add_token(token_type, lexeme, start_column)

            self.current_column += len(lexeme)


    def add_token(self, token_type, lexeme, column):
        self.tokens.append(Token(token_type, lexeme, self.current_line, column))
