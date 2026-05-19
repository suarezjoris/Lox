# Code-Interpreter

A from-scratch implementation of the **Lox** programming language in Python, following the book [*Crafting Interpreters*](https://craftinginterpreters.com/) by Robert Nystrom.

The project is split into two independent parts that mirror the book's structure:

| Part | Approach | Entry point |
|------|----------|-------------|
| `part1/` | Tree-walking interpreter (jlox-style) | `part1/lox.py` |
| `part2/` | Bytecode virtual machine (clox-style) | `part2/lox_vm.py` |

---

## Features

### Part 1 — Tree-walking interpreter
- **Scanner** — tokenises Lox source code into a token stream
- **Parser** — builds an Abstract Syntax Tree (AST) from the token stream
- **AST nodes** — typed node definitions for every expression and statement
- **Resolver** — static variable-resolution pass (scope analysis)
- **Interpreter** — walks the AST and evaluates each node at runtime
- **Environment** — lexically-scoped variable storage with closure support

### Part 2 — Bytecode VM
- **Scanner** — single-pass scanner that feeds directly into the compiler
- **Compiler** — compiles Lox source to bytecode in one pass
- **Chunk** — bytecode container (instructions + constant pool)
- **Value** — dynamic value representation
- **VM** — register-free stack-based virtual machine that executes chunks

---

## Requirements

- Python 3.10+
- No third-party dependencies (pure standard library)

---

## Installation

```bash
git clone https://github.com/Seiya380/Code-Interpreter.git
cd Code-Interpreter
```

No `pip install` step is needed — the project has no external dependencies.

---

## Usage

### Run a Lox script (part 1)

```bash
python part1/lox.py path/to/script.lox
```

### Start a Lox REPL (part 1)

```bash
python part1/lox.py
```

### Run a Lox script with the bytecode VM (part 2)

```bash
python part2/lox_vm.py path/to/script.lox
```

### Example Lox program

```lox
// hello.lox
var greeting = "Hello, world!";
print greeting;

fun fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

print fibonacci(10);
```

---

## Project Structure

```
Code-Interpreter/
├── part1/                  # Tree-walking interpreter
│   ├── lox.py              # Entry point & error reporting
│   ├── scanner.py          # Lexer / tokeniser
│   ├── ast_nodes.py        # AST node definitions
│   ├── parser.py           # Recursive-descent parser
│   ├── resolver.py         # Variable resolution pass
│   ├── environment.py      # Scoped variable storage
│   └── interpreter.py      # AST-walking evaluator
└── part2/                  # Bytecode virtual machine
    ├── lox_vm.py           # Entry point
    ├── scanner.py          # Single-pass scanner
    ├── compiler.py         # Source-to-bytecode compiler
    ├── chunk.py            # Bytecode chunk & constant pool
    ├── value.py            # Value representation
    └── vm.py               # Stack-based VM
```

---

## Running Tests

```bash
pytest
```

Tests are not yet written — contributions welcome!

---

## License

MIT — see [LICENSE](LICENSE).
