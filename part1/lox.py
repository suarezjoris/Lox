import sys
from part1.scanner import *
from part1.parser import *
from part1.interpreter import *

def run(source):
    tokens = Scanner(source).scan_tokens()
    statements = Parser(tokens).parse()
    Interpreter().interpret(statements)

if len(sys.argv) == 2:
    run(open(sys.argv[1]).read())
elif len(sys.argv) == 1:
    while True:
      line = input("> ")
      run(line)

