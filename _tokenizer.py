
from tokenize import generate_tokens, TokenInfo, NEWLINE

def tokenize_file(path: str) -> list[TokenInfo]:
    with open(path, 'r') as file:
        token_list = list(generate_tokens(file.readline))
    return token_list

def filter_tokens(token_list: list[TokenInfo]) -> list[TokenInfo]:
    return list(filter(lambda token: token.line != '\n', token_list))

def seperate_into_lines(token_list: list[TokenInfo]) -> list[list[TokenInfo]]:
    lines = list()
    current_line = list()
    for token in token_list:
        if token.type == NEWLINE:
            lines.append(list(current_line))
            current_line.clear()
        else:
            current_line.append(token)
    return lines

def tokenize(path: str) -> list[list[TokenInfo]]:
    token_list = tokenize_file(path)
    filtered_token_list = filter_tokens(token_list)
    return seperate_into_lines(filtered_token_list)