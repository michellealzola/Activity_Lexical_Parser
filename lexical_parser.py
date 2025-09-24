import re

# --- Token patterns (order matters: longer first) ---
'''
This is just a reminder: when building regex patterns for tokens, you need to list the longer 
or more specific ones first.
Example: if you want >= recognized as a single operator, you must match it before > 
(otherwise the regex might grab the > first and leave = behind).
'''

KEYWORDS = r'\b(?:def|if|else|elif|return|while|for|in|and|or|not|True|False|None)\b'
BUILTIN  = r'\bprint\b'

# Each entry = (token_name, regex_pattern)
TOKEN_SPEC = [
    ("STRING",     r'(?:[fF]?)"(?:[^"\\\n]|\\.)*"'),  # "text" or f"..."
    ("BADSEQ",     r'\)\)'),                          # special: double ')'
    ("KEYWORD",    KEYWORDS),
    ("BUILTIN",    BUILTIN),
    ("NUMBER",     r'\d+(?:\.\d+)?'),
    ("IDENT",      r'[A-Za-z_]\w*'),
    ("AUGASSIGN",  r'(?:\+=|-=|\*=|/=)'),
    ("EQEQ",       r'=='),
    ("NEQ",        r'!='),
    ("LE",         r'<='),
    ("GE",         r'>='),
    ("ASSIGN",     r'='),
    ("LT",         r'<'),
    ("GT",         r'>'),
    ("PLUS",       r'\+'),
    ("MINUS",      r'-'),
    ("STAR",       r'\*'),
    ("SLASH",      r'/'),
    ("LPAREN",     r'\('),
    ("RPAREN",     r'\)'),
    ("COMMA",      r','),
    ("COLON",      r':'),
    ("NEWLINE",    r'\n'),
    ("SKIP",       r'[ \t]+'),
    ("MISMATCH",   r'.'),                              # anything else => error
]
MASTER_RE = re.compile('|'.join(f'(?P<{n}>{p})' for n, p in TOKEN_SPEC))
'''
Explanation:
- for n, p in TOKEN_SPEC --> loop through all (name, pattern) pairs.
- (?P<name>pattern) creates a named group called "name" with the pattern "pattern"
-- Example: if n = "NUMBER" and p = r'\d+', the result is: (?P<NUMBER>\d+)
- | creates a "union" of all the patterns, so that the regex will match any of them
- re.compile() turns the regex into a "compiled" object that can be used for matching
'''

FRIENDLY = {
    "KEYWORD":   ("Keyword", "Language reserved word"),
    "BUILTIN":   ("Built-in Function", "Built-in name"),
    "IDENT":     ("Identifier", "Name of variable/function"),
    "NUMBER":    ("Numeric Literal", "Integer/float constant"),
    "STRING":    ("String Literal", "Quoted text"),
    "ASSIGN":    ("Assignment Operator", "Assigns a value"),
    "AUGASSIGN": ("Augmented Assignment", "Op-and-assign (e.g., -=)"),
    "EQEQ":      ("Relational Operator", "Equality (==)"),
    "NEQ":       ("Relational Operator", "Not-equal (!=)"),
    "LE":        ("Relational Operator", "Less-or-equal (<=)"),
    "GE":        ("Relational Operator", "Greater-or-equal (>=)"),
    "LT":        ("Relational Operator", "Less-than (<)"),
    "GT":        ("Relational Operator", "Greater-than (>)"),
    "PLUS":      ("Addition Operator", "Adds right to left"),
    "MINUS":     ("Subtraction Operator", "Subtracts right from left"),
    "STAR":      ("Multiplication Operator", "Multiplies"),
    "SLASH":     ("Division Operator", "Divides"),
    "LPAREN":    ("Delimiter", "Opening parenthesis"),
    "RPAREN":    ("Delimiter", "Closing parenthesis"),
    "COMMA":     ("Separator", "Separates items/args"),
    "COLON":     ("Delimiter", "Starts an indented block"),
    "NEWLINE":   ("Delimiter", "Line break"),
}

def tokenize(text: str):
    tokens, errors = [], []
    for m in MASTER_RE.finditer(text):
        kind, lexeme = m.lastgroup, m.group()
        if kind in ("SKIP", "NEWLINE"):
            if kind == "NEWLINE":
                tokens.append((kind, "\\n"))
            continue
        if kind == "BADSEQ":
            errors.append(f"Error, {lexeme} is not recognized as a token")
            continue
        if kind == "MISMATCH":
            errors.append(f"Error, {lexeme} is not recognized as a token")
            continue
        tokens.append((kind, lexeme))
    return tokens, errors

def print_tokens_table(tokens):
    if not tokens:
        return
    print("Tokenization Table")
    print(f"{'Lexeme':<28}{'Token':<26}{'Explanation'}")
    print("-" * 80)
    for kind, lexeme in tokens:
        token_name, expl = FRIENDLY.get(kind, (kind, ""))
        print(f"{lexeme:<28}{token_name:<26}{expl}")

def Main():
    samples = [
        # No error
        "inventory = 50",
        # Error: extra closing paren
        "inventory = inventory - 1))",
        # No error: print + string + variable
        'print("Remaining Inventory: " + inventory)',
        # Error: unknown symbol $
        "price = $99",
    ]

    print("=== Demo Cases (with error examples) ===")
    for i, code in enumerate(samples, 1):
        print(f"\nINPUT #{i}: {code}")
        tokens, errors = tokenize(code)
        if errors:
            for e in errors:
                print(e)
        else:
            print("No lexical errors detected")
        print_tokens_table(tokens)
        print()

if __name__ == "__main__":
    Main()
