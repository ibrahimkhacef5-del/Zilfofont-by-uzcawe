cat > zalfofont/lexer.py << 'ENDOFFILE'
"""Lexer - تحويل النص إلى tokens"""
from .tokens import Token, TokenType, KEYWORDS


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def peek(self, offset=0):
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return ""

    def advance(self):
        if self.pos >= len(self.source):
            return ""
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def skip_whitespace(self):
        while self.peek() in (" ", "\t", "\r"):
            self.advance()

    def skip_comment(self):
        if self.peek() == "#":
            while self.peek() and self.peek() != "\n":
                self.advance()
            return True
        if self.peek() == "/" and self.peek(1) == "*":
            self.advance()
            self.advance()
            while self.peek():
                if self.peek() == "*" and self.peek(1) == "/":
                    self.advance()
                    self.advance()
                    return True
                self.advance()
            raise LexerError(f"تعليق غير مغلق في السطر {self.line}")
        return False

    def read_string(self):
        quote = self.advance()
        result = ""
        while self.peek() and self.peek() != quote:
            ch = self.advance()
            if ch == "\\":
                next_ch = self.advance()
                result += {
                    "n": "\n", "t": "\t", "r": "\r",
                    "\\": "\\", "'": "'", '"': '"',
                }.get(next_ch, next_ch)
            else:
                result += ch
        if self.peek() != quote:
            raise LexerError(f"نص غير مغلق في السطر {self.line}")
        self.advance()
        return result

    def read_number(self):
        result = ""
        if self.peek() == "0" and self.peek(1).lower() == "x":
            result = self.advance() + self.advance()
            while self.peek() and (self.peek().isdigit()
                                    or self.peek().lower() in "abcdef"):
                result += self.advance()
            return result
        while self.peek() and (self.peek().isdigit() or self.peek() == "."):
            result += self.advance()
        return result

    def read_identifier(self):
        result = ""
        while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
            result += self.advance()
        return result

    def tokenize(self):
        while self.pos < len(self.source):
            self.skip_whitespace()

            if not self.peek():
                break

            if self.peek() == "#" or (self.peek() == "/" and self.peek(1) == "*"):
                self.skip_comment()
                continue

            ch = self.peek()
            line, col = self.line, self.column

            if ch == "{":
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, "{", line, col))
            elif ch == "}":
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, "}", line, col))
            elif ch == "(":
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, "(", line, col))
            elif ch == ")":
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ")", line, col))
            elif ch == "[":
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, "[", line, col))
            elif ch == "]":
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, "]", line, col))
            elif ch == ":":
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ":", line, col))
            elif ch == ",":
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ",", line, col))
            elif ch == ";":
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ";", line, col))
            elif ch == "+":
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, "+", line, col))
            elif ch == "-":
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, "-", line, col))
            elif ch == "*":
                self.advance()
                self.tokens.append(Token(TokenType.STAR, "*", line, col))
            elif ch == "/":
                self.advance()
                self.tokens.append(Token(TokenType.SLASH, "/", line, col))
            elif ch == "=":
                self.advance()
                if self.peek() == "=":
                    self.advance()
                    self.tokens.append(Token(TokenType.EQUAL_EQUAL, "==", line, col))
                else:
                    self.tokens.append(Token(TokenType.EQUAL, "=", line, col))
            elif ch == "!" and self.peek(1) == "=":
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, "!=", line, col))
            elif ch in ('"', "'"):
                s = self.read_string()
                self.tokens.append(Token(TokenType.STRING, s, line, col))
            elif ch.isdigit():
                n = self.read_number()
                if n.lower().startswith("0x"):
                    self.tokens.append(Token(TokenType.HEX, n, line, col))
                else:
                    self.tokens.append(Token(TokenType.NUMBER, n, line, col))
            elif ch.isalpha() or ch == "_":
                ident = self.read_identifier()
                if ident in KEYWORDS:
                    if ident in ("true", "false"):
                        self.tokens.append(Token(TokenType.BOOLEAN, ident, line, col))
                    else:
                        self.tokens.append(Token(KEYWORDS[ident], ident, line, col))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, ident, line, col))
            else:
                raise LexerError(
                    f"رمز غير معروف: {ch!r} في السطر {line}:{col}"
                )

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


def tokenize(source):
    return Lexer(source).tokenize()
ENDOFFILE

echo "✅ lexer.py"
