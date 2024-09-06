from simple_language import TokenType

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.end_encountered = False

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
        
    def check_end_statement(self, current_token):           
        if self.end_encountered:
            raise Exception("Erro de semântica: 'END' já foi encontrado.")
        self.end_encountered = True