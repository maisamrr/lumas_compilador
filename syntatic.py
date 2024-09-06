from simple_language import TokenType
from semantic import SemanticAnalyzer
class Parser:
    def __init__(self, tokens, semantic_analyzer):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance_next_token()
        self.last_line_number = 0
        self.semantic_analyzer = semantic_analyzer

    def advance_next_token(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self): # programa inteiro
        while self.current_token is not None:
            self.statement()

    def statement(self): # declaracoes individuais
        self.check_line_number()
        self.advance_next_token()

        if self.current_token.token_type == TokenType.LET:
            self.let_statement()
        elif self.current_token.token_type == TokenType.IF:
            self.if_statement()
        elif self.current_token.token_type == TokenType.GOTO:
            self.goto_statement()
        elif self.current_token.token_type == TokenType.PRINT:
            self.print_statement()
        elif self.current_token.token_type == TokenType.REM:
            self.rem_statement()
        elif self.current_token.token_type == TokenType.INPUT:
            self.input_statement()
        elif self.current_token.token_type == TokenType.END:
            self.end_statement()
            return
        else:
            self.error_statement(f"Declaração inválida: '{self.current_token.symbol_address}'")

    def let_statement(self): 
        self.advance_next_token()
        if self.current_token.token_type == TokenType.VARIABLE:
            variable_name = self.current_token.symbol_address

            if variable_name in self.semantic_analyzer.symbol_table:
                # variavel ja declarada
                self.semantic_analyzer.check_variable_assignment(variable_name, self.current_token.line, self.current_token.column)
            else:
                # variavel declarada pela 1a vez
                self.semantic_analyzer.declare_variable(variable_name, self.current_token.line, self.current_token.column)
            
            self.advance_next_token()
            if self.current_token.token_type == TokenType.ASSIGNMENT:
                self.advance_next_token()
                self.expression()
                self.semantic_analyzer.initialize_variable(variable_name, self.current_token.line, self.current_token.column)
            else:
                self.error_statement("Esperado '=' depois da variável")
        else:
            self.error_statement("Deve haver uma variável após LET")

    def error_statement(self, message):
        raise Exception(f"Erro de sintaxe: {message} na linha {self.current_token.line}, coluna {self.current_token.column}")

    def if_statement(self):
        self.advance_next_token() 
        self.relational_expression()
        if self.current_token.token_type == TokenType.GOTO:
            self.advance_next_token()
            if self.current_token.token_type == TokenType.INTEGER:
                self.advance_next_token()
            else:
                self.error_statement("Esperado número de linha após GOTO")
        else:
            self.error_statement("Esperado GOTO após a condição")
    
    def goto_statement(self):
        self.advance_next_token()
        if self.current_token.token_type == TokenType.INTEGER:
            self.advance_next_token()
        else:
            self.error_statement("Espera-se um número de linha após o GOTO")

    def print_statement(self):
        self.advance_next_token()
        self.expression()
    
    def rem_statement(self):
        self.advance_next_token()
        
    def input_statement(self):
        self.advance_next_token()  
        if self.current_token.token_type == TokenType.VARIABLE:
            variable_name = self.current_token.symbol_address
            if variable_name in self.semantic_analyzer.symbol_table:
                self.semantic_analyzer.check_variable_assignment(variable_name, self.current_token.line, self.current_token.column)
            else:
                self.semantic_analyzer.declare_variable(variable_name, self.current_token.line, self.current_token.column)
                self.semantic_analyzer.initialize_variable(variable_name, self.current_token.line, self.current_token.column)
            self.advance_next_token() 
        else:
            self.error_statement("Espera-se uma variável após o INPUT")

    def expression(self): # variavel, inteiro ou operacao
        if self.current_token.token_type == TokenType.SUBTRACT:
            self.advance_next_token()
            if self.current_token.token_type == TokenType.INTEGER and self.current_token.symbol_address == '1':
                self.advance_next_token()
            else:
                self.error_statement("Espera-se o número '1' após '-'")
        elif self.current_token.token_type == TokenType.VARIABLE:
            variable_name = self.current_token.symbol_address
            self.semantic_analyzer.check_variable_usage(variable_name, self.current_token.line, self.current_token.column)
            self.advance_next_token()

            if self.current_token.token_type in (TokenType.ADD, TokenType.SUBTRACT, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
                self.advance_next_token()
                self.expression()
        elif self.current_token.token_type == TokenType.INTEGER:
            self.advance_next_token()
            if self.current_token.token_type in (TokenType.ADD, TokenType.SUBTRACT, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
                self.advance_next_token()
                self.expression()
        else:
            self.error_statement("Expressão inválida")

    def end_statement(self):
        self.advance_next_token()
        if self.current_token is not None:
            self.error_statement("Não deve haver nenhum token após o END")
        self.semantic_analyzer.check_end_statement(self.current_token)
            
    def check_line_number(self):
        if self.current_token.token_type == TokenType.LINENUMBER:
            current_line_number = self.current_token.symbol_address
            if current_line_number <= self.last_line_number:
                self.error_statement(f"Linha número {current_line_number} não é maior que {self.last_line_number}")
            self.last_line_number = current_line_number
        else:
            self.error_statement("Espera-se um número de linha no início da declaração")

    def relational_expression(self):
        if self.current_token.token_type in (TokenType.VARIABLE, TokenType.INTEGER):
            self.advance_next_token()
        else:
            self.error_statement("Espera-se uma variável ou inteiro antes do operador relacional")

        if self.current_token.token_type in (TokenType.EQ, TokenType.NE, TokenType.GT, TokenType.LT, TokenType.GE, TokenType.LE):
            self.advance_next_token()  
        else:
            self.error_statement("Espera-se um operador relacional")

        if self.current_token.token_type in (TokenType.VARIABLE, TokenType.INTEGER):
            self.advance_next_token()
        else:
            self.error_statement("Espera-se uma variável ou inteiro após o operador relacional")