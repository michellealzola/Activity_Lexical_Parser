import re

# --- Token patterns (order matters) ---
TOKEN_SPEC = [
    ("STRING",   r'"[^"\n]*"'),          # "text"
    ("BADSEQ",   r'\)\)'),               # special-case: double close paren
    ("NUMBER",   r'\d+(?:\.\d+)?'),      # 50, 3.14
    ("BUILTIN",  r'\bprint\b'),          # built-in function
    ("IDENT",    r'[A-Za-z_]\w*'),       # inventory, _tmp1
    ("ASSIGN",   r'='),                  # =
    ("PLUS",     r'\+'),                 # +
    ("MINUS",    r'-'),                  # -
    ("STAR",     r'\*'),                 # *
    ("SLASH",    r'/'),                  # /
    ("COMMA",    r','),                  # ,
    ("LPAREN",   r'\('),                 # (
    ("RPAREN",   r'\)'),                 # )
    ("NEWLINE",  r'\n'),                 # newline
    ("SKIP",     r'[ \t]+'),             # spaces/tabs
    ("MISMATCH", r'.'),                  # anything else
]
MASTER_RE = re.compile('|'.join(f'(?P<{n}>{p})' for n, p in TOKEN_SPEC))

# Friendly names for Tokenization Table
FRIENDLY = {
    "IDENT":   ("Identifier", "Variable name"),
    "ASSIGN":  ("Assignment Operator", "Assigns value to variable"),
    "NUMBER":  ("Numeric Literal", "Integer/float constant"),
    "MINUS":   ("Subtraction Operator", "Subtracts right operand from left operand"),
    "PLUS":    ("Addition Operator", "Adds right operand to left operand"),
    "BUILTIN": ("Built-in Function", "Built-in output function"),
    "LPAREN":  ("Delimiter", "Function call using parenthesis"),
    "RPAREN":  ("Delimiter", "Function call closing parenthesis"),
    "COMMA":   ("Separator", "Separates items or arguments"),
    "STRING":  ("String Literal", "Message to display"),
    "NEWLINE": ("Delimiter", "Marks beginning of indented block"),
}

def tokenize(line: str):
    tokens, errors = [], []
    for m in MASTER_RE.finditer(line):
        kind, lexeme = m.lastgroup, m.group()
        if kind == "SKIP":
            continue
        elif kind == "BADSEQ":
            errors.append(f"Error, {lexeme} is not recognized as a token")
        elif kind == "MISMATCH":
            errors.append(f"Error, {lexeme} is not recognized as a token")
        else:
            tokens.append((kind, lexeme))
    return tokens, errors

def print_tokens_table(tokens):
    if not tokens:
        return
    print("\nTokenization Table")
    print(f"{'Lexeme':<20}{'Token':<25}{'Explanation'}")
    print("-" * 65)
    for kind, lexeme in tokens:
        token_name, expl = FRIENDLY.get(kind, (kind, ""))
        print(f"{lexeme:<20}{token_name:<25}{expl}")

# --- Demo driver for the 3 inputs ---
def Main():
    # Input #1
    line1 = "inventory = 50"
    t1, e1 = tokenize(line1)
    print(f"INPUT: {line1}")
    if e1:
        for err in e1: print(err)
    else:
        print("No lexical errors detected")
    print_tokens_table(t1)
    print()

    # Input #2
    line2 = "inventory = inventory - 1))"
    t2, e2 = tokenize(line2)
    print(f"INPUT: {line2}")
    if e2:
        for err in e2: print(err)
    else:
        print("No lexical errors detected")
    print_tokens_table(t2)
    print()

    # Input #3
    line3 = 'print("Remaining Inventory: " + inventory)'
    t3, e3 = tokenize(line3)
    print(f"INPUT: {line3}")
    if e3:
        for err in e3: print(err)
    else:
        print("No lexical errors detected")
    print_tokens_table(t3)
    print()

if __name__ == "__main__":
    Main()
