from lexic import SimpleLexer
from syntatic import Parser
from semantic import SemanticAnalyzer

def main():
    lexer = SimpleLexer()
    my_simple_file = "arquivo5.txt"
    lexer.process_txt(my_simple_file)
    
    print("Tokens gerados:")
    for token in lexer.tokens:
        print(token)

    semantic_analyzer = SemanticAnalyzer()
    
    parser = Parser(lexer.tokens, semantic_analyzer)
    try:
        parser.parse()
        print("Parsing e análise semântica realizados com sucesso.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()