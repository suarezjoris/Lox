from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()

    VAR = auto()
    FUN = auto()
    IF = auto()
    ELSE = auto()
    RETURN = auto()
    FOR = auto()
    WHILE = auto()
    TRUE = auto()
    FALSE = auto()
    NIL = auto()
    PRINT = auto()
    AND = auto()
    OR = auto()
    CLASS = auto()
    SUPER = auto()
    THIS = auto()

    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    EOF = auto()

KEYWORDS = {
    "var":TokenType.VAR,
    "if":TokenType.IF,
    "else":TokenType.ELSE,
    "return":TokenType.RETURN,
    "for":TokenType.FOR,
    "while":TokenType.WHILE,
    "true":TokenType.TRUE,
    "false":TokenType.FALSE,
    "nil":TokenType.NIL,
    "print":TokenType.PRINT,
    "and":TokenType.AND,
    "or":TokenType.OR,
    "class":TokenType.CLASS,
    "super":TokenType.SUPER,
    "this":TokenType.THIS,
    "fun":TokenType.FUN

}

@dataclass 
class Token:
    type: TokenType
    lexeme: str
    value: object
    line: int

class Scanner:
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
    
    def scan_tokens(self):
      while self.current < len(self.source):
          self.start = self.current
          self._scan_token()
      self.tokens.append(Token(TokenType.EOF, "", None, self.line))
      return self.tokens

    def _scan_token(self):
        c = self.source[self.current]
        self.current += 1
        if c.isdigit():
            self._scan_number()
        elif c.isalnum() or c == '_':
            self._scan_identifier()
        elif c == '(':
            self._add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self._add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self._add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self._add_token(TokenType.RIGHT_BRACE)
        elif c == ';':
            self._add_token(TokenType.SEMICOLON)
        elif c == ',':
            self._add_token(TokenType.COMMA)
        elif c == '+':
            self._add_token(TokenType.PLUS)
        elif c == '-':
            self._add_token(TokenType.MINUS)
        elif c == '*':
            self._add_token(TokenType.STAR)
        elif c == '=':
            self._add_token(TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL)
        elif c == '!':
            self._add_token(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)
        elif c == '<':
            self._add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
        elif c == '>':
            self._add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)
        elif c == '/':
            if self._match('/'):
                # comment: skip until end of line
                while self.current < len(self.source) and self.source[self.current] != '\n':
                    self.current += 1
            else:
                self._add_token(TokenType.SLASH)
        elif c == '"':
            self._scan_string()
        elif c in (' ', '\r', '\t'):
            pass
        elif c in ('\n'):
            self.line += 1 
        

    def _add_token(self, type, value=None):
      lexeme = self.source[self.start:self.current]
      self.tokens.append(Token(type, lexeme, value, self.line))

    def _match(self, expected):
      if self.current >= len(self.source):
          return False
      if self.source[self.current] != expected:
          return False
      self.current += 1
      return True

    def _scan_string(self):
        while self.current < len(self.source) and self.source[self.current] != '"':
            if self.source[self.current] == '\n':
                self.line += 1
            self.current += 1
            
        if self.current >= len(self.source):
            print(f"Unterminated string at line {self.line}")
        self.current += 1  # consume the closing "
        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, value)
        return
    
    def _scan_number(self):
        # consume integer part
        while self.current < len(self.source) and self.source[self.current].isdigit():
            self.current += 1
            
        # check for decimal part
        if (self.current < len(self.source) and self.source[self.current] == '.' 
        and self.current + 1 < len(self.source)
        and self.source[self.current + 1].isdigit()):
            self.current += 1  # consume '.'
        while self.current < len(self.source) and self.source[self.current].isdigit():
            self.current += 1
        value = float(self.source[self.start:self.current])
        self._add_token(TokenType.NUMBER, value)

    def _scan_identifier(self):
        # consume integer part
        while self.current < len(self.source) and (self.source[self.current].isalnum() or self.source[self.current] == '_'):
            self.current += 1
        word = self.source[self.start:self.current] 
        self._add_token(KEYWORDS.get(word, TokenType.IDENTIFIER))