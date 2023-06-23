
def get_line_ln(line_char: str, edge_char: str, line_len: int = 80):
    return get_line(line_char, edge_char, line_len) + '\n'

def get_line(line_char: str, edge_char: str, line_len: int = 80):
    padding_len = line_len - 2
    padding = line_char * padding_len
    return f"{edge_char}{padding}{edge_char}"

def print_line(line_char: str, edge_char: str, line_len: int = 80):
    print(get_line(line_char, edge_char, line_len))

def get_form_ln(line: str) -> str:
    return get_form(line) + '\n'

def get_form(line: str) -> str:
    line_len = len(line)
    padding_len = 80 - (line_len + 4)
    padding = " " * padding_len
    return f"| {line}{padding} |"

def print_form(line: str):
    print(get_form(line))
