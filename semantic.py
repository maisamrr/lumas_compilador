from simple_language import TokenType

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.end_encountered = False
        self.last_line_number = -1
        self.valid_line_numbers = set()

    def declare_variable(self, variable_name, line, column):
        if variable_name in self.symbol_table:
            # reatribuições ok
            raise Exception(f"Erro de semântica: variável '{variable_name}' já foi declarada. Linha: {line}, Coluna: {column}")
        self.symbol_table[variable_name] = {"type": "int", "initialized": False}

    def initialize_variable(self, variable_name, line, column):
        if variable_name not in self.symbol_table:
            raise Exception(f"Erro de semântica: variável '{variable_name}' não foi declarada. Linha: {line}, Coluna: {column}")
        self.symbol_table[variable_name]["initialized"] = True

    def check_variable_usage(self, variable_name, line, column):
        if variable_name not in self.symbol_table:
            raise Exception(f"Erro de semântica: variável '{variable_name}' não foi declarada. Linha: {line}, Coluna: {column}")
        if not self.symbol_table[variable_name]["initialized"]:
            raise Exception(f"Erro de semântica: variável '{variable_name}' foi declarada, mas não foi inicializada. Linha: {line}, Coluna: {column}")

    def check_variable_assignment(self, variable_name, line, column):
        # permitir atribuição mesmo com variável já inicializada
        if variable_name not in self.symbol_table:
            raise Exception(f"Erro de semântica: variável '{variable_name}' não foi declarada. Linha: {line}, Coluna: {column}")
        
    def check_end_statement(self):           
        if self.end_encountered:
            raise Exception("Erro de semântica: 'END' já foi encontrado.")
        self.end_encountered = True
        
    def check_line_number_order(self, current_line_number, line, column):
        if current_line_number <= self.last_line_number:
            raise Exception(f"Erro de semântica: A linha {current_line_number} não é maior que a linha anterior ({self.last_line_number}). Linha: {line}, Coluna: {column}")
        self.last_line_number = current_line_number
    
    def register_line_number(self, line_number):
        self.valid_line_numbers.add(line_number)

    def check_goto_line(self, line_number, line, column):
        if line_number not in self.valid_line_numbers:
            raise Exception(f"Erro de semântica: O GOTO referencia um número de linha inválido ({line_number}). Linha: {line}, Coluna: {column}")
        
    def check_line_number(self):
        if self.current_token.token_type == TokenType.LINENUMBER:
            current_line_number = self.current_token.symbol_address
            self.semantic_analyzer.register_line_number(current_line_number)
            self.semantic_analyzer.check_line_number_order(current_line_number, self.current_token.line, self.current_token.column)
        else:
            self.error_statement("Espera-se um número de linha no início da declaração")

