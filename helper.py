def read_input_file(input_file_name):
    """Reads a context-free grammar from a file and returns it as a dictionary."""
    grammar = {}
    with open(input_file_name, 'r', encoding='utf-8') as file:
        print("Reading input file...")
        for line in file:
            line = line.strip()
            if line:
                non_terminal, productions = line.split('->')
                grammar[non_terminal.strip()] = [production.strip() for production in productions.split('|')]
    return grammar


# Save the CNF grammar to a file
def save_grammar(grammar, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        for var, prods in grammar.items():
            file.write(var + ' -> ' + ' | '.join(prods) + '\n')