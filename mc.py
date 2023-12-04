
from argparse import ArgumentParser

from _interpreter import create_interpreter, Interpreter
from _parser import parse
from _tokenizer import tokenize

parser = ArgumentParser()
parser.add_argument('file', help='The file to execute, must be a mc file')

args = parser.parse_args()
path = args.file if args.file.endswith('.mc') else args.file + '.mc'

interpreter: Interpreter = create_interpreter(parse(tokenize(path)))

interpreter.start()