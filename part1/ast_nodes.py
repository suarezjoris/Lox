from dataclasses import dataclass
from part1.scanner import Token

@dataclass
class Binary:
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Unary:
    operator: Token
    operand: Expr

@dataclass
class Grouping:
    expression:Expr

@dataclass
class Literal:
    value: object

@dataclass
class Variable:
    name: Token

@dataclass
class Call:
    callee: Expr
    paren: Token
    arguments: list

@dataclass
class Print:
    expression: Expr

@dataclass
class Var:
    name: Token
    initializer: Expr

@dataclass
class If:
    condition: Expr
    then_branch: Expr
    else_branch: Expr

@dataclass
class While:
    condition: Expr
    body: Expr

@dataclass
class Function:
    name: Token
    params: list
    body: list

@dataclass
class Return:
    keyword: Token
    value: Expr

@dataclass
class Block:
    statements: list

@dataclass
class Expression:
    expression: Expr
