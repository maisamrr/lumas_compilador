from lexic import SimpleLexer
from syntatic import Parser

def main():
    lexer = SimpleLexer()

    my_simple_file = "arquivo1.txt"
    lexer.process_txt(my_simple_file)
    
    for token in lexer.tokens:
        print(token)

    parser = Parser(lexer.tokens)
    try:
        parser.parse()
        print("Parsing realizado com sucesso.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()