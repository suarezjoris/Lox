from part1.environment import *
from part1.scanner import TokenType

class Interpreter:
    def __init__(self):
        self.environment = Environment()  # global scope

    def interpret(self, statements):
        for i in statements:
            self.execute(i)

    def execute(self, stmt):
        method = getattr(self, 'visit_' + type(stmt).__name__)
        return method(stmt)
        
    def evaluate(self, expr):
        method = getattr(self, 'visit_' + type(expr).__name__)
        return method(expr)

    def visit_Grouping(self, expr):
        return self.evaluate(expr.expression)

    def visit_Literal(self, expr):
      return expr.value

    def visit_Unary(self, expr):
        right = self.evaluate(expr.operand)
        if expr.operator.type == TokenType.MINUS:
            return -right
        if expr.operator.type == TokenType.BANG:
            return not right

    def visit_Binary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.PLUS:
            return left + right
        if expr.operator.type == TokenType.MINUS:
            return left - right
        if expr.operator.type == TokenType.STAR:
            return left * right
        if expr.operator.type == TokenType.SLASH:
            return left / right
        if expr.operator.type == TokenType.EQUAL_EQUAL:
            if left == right:
                return True
            else:
                return False
        if expr.operator.type == TokenType.BANG_EQUAL:
            if left != right:
                return True
            else:
                return False
        if expr.operator.type == TokenType.LESS:
            if left < right:
                return True
            else:
                return False
        if expr.operator.type == TokenType.LESS_EQUAL:
            if left <= right:
                return True
            else:
                return False
        if expr.operator.type == TokenType.GREATER:
            if left > right:
                return True
            else:
                return False
        if expr.operator.type == TokenType.GREATER_EQUAL:
            if left >= right:
                return True
            else:
                return False

    def visit_Print(self, expr):
        output = self.evaluate(expr.expression)
        print(output)
        return

    def visit_Expression(self, expr):
        self.evaluate(expr.expression)

    def visit_Var(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_Variable(self, stmt):
        output = self.environment.get(stmt.name)
        return output
    
    def visit_Block(self, stmt):
        previous = self.environment
        self.environment = Environment(enclosing=previous)
        try:
            for s in stmt.statements:
                self.execute(s)
        finally:
            self.environment = previous

    def visit_If(self, stmt):
        condition = self.evaluate(stmt.condition)
        if condition:
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch) 
        return

    def visit_While(self, stmt):
        while self.evaluate(stmt.condition):
            self.execute(stmt.body) 
        return

    def visit_Function(self, stmt):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)

    def visit_Return(self,stmt):
        if stmt.value == None:
            return
        else:
            value = self.evaluate(stmt.value)
            raise ReturnException(value)
    
    def visit_Call(self, expr):
        args = []
        callee = self.evaluate(expr.callee)
        for arg in expr.arguments:
            args.append(self.evaluate(arg))
        return callee.call(self, args)


class LoxFunction:
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        env = Environment(enclosing=self.closure)
        for param, arg in zip(self.declaration.params, arguments):
            env.define(param.lexeme, arg)
        previous = interpreter.environment
        interpreter.environment = env
        try:
            for s in self.declaration.body:
                interpreter.execute(s)
        except ReturnException as e:
            interpreter.environment = previous
            return e.value
        interpreter.environment = previous

class ReturnException(Exception):
      def __init__(self, value):
          self.value = value