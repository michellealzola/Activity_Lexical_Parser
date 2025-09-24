import re

# --- Token patterns (order matters: longer first) ---

# This is just a reminder: when building regex patterns for tokens, you need to list the longer
# or more specific ones first.
# Example: if you want >= recognized as a single operator, you must match it before >
# (otherwise the regex might grab the > first and leave = behind).


KEYWORDS = r'\b(?:def|if|else|elif|return|while|for|in|and|or|not|True|False|None)\b'
BUILTIN  = r'\bprint\b'

# Each entry = (token_name, regex_pattern)
TOKEN_SPEC = [
    ("STRING", r"(?:[fF]?)'(?:[^'\\\n]|\\.)*'|(?:[fF]?)\"(?:[^\"\\\n]|\\.)*\""),  # "text" or f"..."
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


# Explanation fo the above code:
# - for n, p in TOKEN_SPEC --> loop through all (name, pattern) pairs.
# - (?P<name>pattern) creates a named group called "name" with the pattern "pattern"
# -- Example: if n = "NUMBER" and p = r'\d+', the result is: (?P<NUMBER>\d+)
# - | creates a "union" of all the patterns, so that the regex will match any of them
# - re.compile() turns the regex into a "compiled" object that can be used for matching
#
#
# The FRIENDLY dict is just a lookup table that translates the technical token type names
# (like "IDENT" or "EQEQ") into something more human-readable for the Tokenization table.
# It's not strictly necessary, but it helps improve the user experience.


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
    # This function takes a line of source code (text)
    # and returns two lists:
    #   1. tokens = valid tokens recognized
    #   2. errors = error messages for invalid tokens

    tokens, errors = [], []   # lists to collect results

    # Go through the input text, matching against MASTER_RE (the big regex)
    for m in MASTER_RE.finditer(text):
        kind, lexeme = m.lastgroup, m.group()
        # kind   = which token type matched (e.g., IDENT, NUMBER, ASSIGN)
        # lexeme = the actual text from the source code (e.g., 'inventory', '50', '=')

        # --- Handle special cases ---

        # Ignore whitespace and tabs, but if it's a newline,
        # keep it as a token (so we know where line breaks are)
        if kind in ('SKIP', 'NEWLINE'):
            if kind == 'NEWLINE':
                tokens.append((kind, '\\n'))
            continue

        # Special error: double closing parenthesis '))'
        if kind == 'BADSEQ':
            errors.append(f'Error, {lexeme} is not recognized as a token')
            continue

        # Any unknown or illegal character
        if kind == 'MISMATCH':
            errors.append(f'Error, {lexeme} is not recognized as a token')
            continue

        # If none of the above, it's a valid token → add to the tokens list
        tokens.append((kind, lexeme))

    # Return both lists: tokens and errors
    return tokens, errors


def print_tokens_table(tokens):
    # This function prints a nicely formatted table of tokens.
    # Input: tokens (a list of (kind, lexeme) pairs from tokenize()).
    # Output: prints a table with Lexeme, Token (friendly name), and Explanation.

    # If there are no tokens, just return (do nothing)
    if not tokens:
        return

    # Print table header
    print('Tokenization Table')
    print(f"{'Lexeme':<28}{'Token':<26}{'Explanation'}")
    print('-' * 80)

    # Loop through each token and print details
    for kind, lexeme in tokens:
        # Look up the friendly name and explanation for this token type
        token_name, expl = FRIENDLY.get(kind, (kind, ''))
        # Print one row of the table with aligned columns
        print(f"{lexeme:<28}{token_name:<26}{expl}")


def Main():
    # --- Part 1: Demo cases for lexical analysis ---
    samples = [
        # No error
        'inventory = 50',
        # Error: extra closing parenthesis
        'inventory = inventory - 1))',
        # Decrease inventory using the correct syntax
        'inventory -= 1',
        # No error: print + string + variable
        'print("Remaining Inventory: " + inventory)',
        # Error: unknown symbol $
        'price = $99',
    ]

    print('=== Demo Cases (with error examples) ===')
    for i, code in enumerate(samples, 1):
        print(f'\nINPUT #{i}: {code}')
        tokens, errors = tokenize(code)

        # Print errors if any were found
        if errors:
            for e in errors:
                print(e)
        else:
            print('No lexical errors detected')

        # Print the tokenization table for this input
        print_tokens_table(tokens)
        print()

    # --- Part 2: Use the lexical parser on activity 1 snippet ---
    print('=== Lexing the short snippet (no execution) ===')
    snippet = (
        'def Main():\n'
        '    inventory = 50\n'
        '    inventory -= 1\n'
        "    print(f'{inventory}')\n"
        '\n'
        "if __name__ == '__main__':\n"
        '    Main()\n'
    )

    print('SOURCE CODE:')
    print(snippet)

    # Feed the whole snippet to the lexer
    tokens, errors = tokenize(snippet)

    if errors:
        for e in errors:
            print(e)
    else:
        print('No lexical errors detected')

    # Show the tokenization table for the snippet
    print_tokens_table(tokens)



# Standard Python entry point check
if __name__ == '__main__':
    Main()