class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, token):
        if token.lexeme in self.values:
            return self.values[token.lexeme]
        if self.enclosing:
            return self.enclosing.get(token)
        raise RuntimeError(f"Undefined variable '{token.lexeme}'.")

    def assign(self, token, value):
        if token.lexeme in self.values:
            self.values[token.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(token, value)
            return
        raise RuntimeError(f"Undefined variable '{token.lexeme}'.")
