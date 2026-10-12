cat > zalfofont/tokens.py << 'ENDOFFILE'
"""تعريف الـ tokens للغة zalfofont"""


class TokenType:
    FONT = "FONT"
    GLYPH = "GLYPH"
    CONTOUR = "CONTOUR"
    POINT = "POINT"
    ANCHOR = "ANCHOR"
    LAYER = "LAYER"
    META = "META"
    CLOSE = "CLOSE"

    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COLON = "COLON"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"

    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"

    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    BOOLEAN = "BOOLEAN"
    HEX = "HEX"

    NEWLINE = "NEWLINE"
    COMMENT = "COMMENT"
    EOF = "EOF"


KEYWORDS = {
    "font": TokenType.FONT,
    "glyph": TokenType.GLYPH,
    "contour": TokenType.CONTOUR,
    "point": TokenType.POINT,
    "anchor": TokenType.ANCHOR,
    "layer": TokenType.LAYER,
    "meta": TokenType.META,
    "close": TokenType.CLOSE,
    "true": TokenType.BOOLEAN,
    "false": TokenType.BOOLEAN,
}


class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line}:{self.column})"
ENDOFFILE

echo "✅ tokens.py"
