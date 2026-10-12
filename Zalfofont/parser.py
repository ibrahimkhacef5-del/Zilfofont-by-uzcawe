cat > zalfofont/parser.py << 'ENDOFFILE'
"""Parser - بناء AST من tokens"""
from .tokens import TokenType
from .ast_nodes import (
    Program, FontDef, GlyphDef, Contour, Point, Anchor
)


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset=0):
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def advance(self):
        tok = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return tok

    def expect(self, type_, value=None):
        tok = self.peek()
        if tok.type != type_:
            raise ParseError(
                f"متوقع {type_}, وجد {tok.type} "
                f"({tok.value!r}) في السطر {tok.line}"
            )
        if value is not None and tok.value != value:
            raise ParseError(
                f"متوقع {value!r}, وجد {tok.value!r} "
                f"في السطر {tok.line}"
            )
        return self.advance()

    def parse(self):
        font = None
        glyphs = []

        while self.peek().type != TokenType.EOF:
            tok = self.peek()
            if tok.type == TokenType.FONT:
                font = self.parse_font()
            elif tok.type == TokenType.GLYPH:
                glyphs.append(self.parse_glyph())
            else:
                raise ParseError(
                    f"متوقع 'font' أو 'glyph', وجد {tok.type} "
                    f"في السطر {tok.line}"
                )

        return Program(font, glyphs)

    def parse_font(self):
        self.expect(TokenType.FONT)
        name = self.expect(TokenType.STRING).value
        self.expect(TokenType.LBRACE)

        properties = {}
        while self.peek().type != TokenType.RBRACE:
            if self.peek().type == TokenType.META:
                self.advance()
                self.expect(TokenType.LBRACE)
                while self.peek().type != TokenType.RBRACE:
                    key = self.expect(TokenType.IDENTIFIER).value
                    self.expect(TokenType.COLON)
                    value = self.parse_value()
                    properties[f"meta.{key}"] = value
                self.expect(TokenType.RBRACE)
            else:
                key = self.expect(TokenType.IDENTIFIER).value
                self.expect(TokenType.COLON)
                value = self.parse_value()
                properties[key] = value

        self.expect(TokenType.RBRACE)
        return FontDef(name, properties)

    def parse_glyph(self):
        self.expect(TokenType.GLYPH)
        name = self.expect(TokenType.STRING).value
        self.expect(TokenType.LBRACE)

        properties = {}
        contours = []
        anchors = []

        while self.peek().type != TokenType.RBRACE:
            tok = self.peek()

            if tok.type == TokenType.CONTOUR:
                contours.append(self.parse_contour())
            elif tok.type == TokenType.ANCHOR:
                anchors.append(self.parse_anchor())
            else:
                key = self.expect(TokenType.IDENTIFIER).value
                self.expect(TokenType.COLON)
                value = self.parse_value()
                properties[key] = value

        self.expect(TokenType.RBRACE)
        return GlyphDef(name, properties, contours, anchors)

    def parse_contour(self):
        self.expect(TokenType.CONTOUR)
        self.expect(TokenType.LBRACE)

        points = []
        closed = False

        while self.peek().type != TokenType.RBRACE:
            tok = self.peek()
            if tok.type == TokenType.POINT:
                self.advance()
                self.expect(TokenType.LPAREN)
                x = self.parse_number()
                self.expect(TokenType.COMMA)
                y = self.parse_number()
                self.expect(TokenType.RPAREN)
                points.append(Point(x, y))
            elif tok.type == TokenType.CLOSE:
                self.advance()
                closed = True
            else:
                raise ParseError(
                    f"متوقع 'point' أو 'close', وجد {tok.type} "
                    f"في السطر {tok.line}"
                )

        self.expect(TokenType.RBRACE)
        return Contour(points, closed)

    def parse_anchor(self):
        self.expect(TokenType.ANCHOR)
        name = self.expect(TokenType.STRING).value
        self.expect(TokenType.LBRACE)

        props = {}
        while self.peek().type != TokenType.RBRACE:
            key = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.COLON)
            props[key] = self.parse_number()

        self.expect(TokenType.RBRACE)
        return Anchor(name, props.get("x", 0), props.get("y", 0))

    def parse_value(self):
        tok = self.peek()
        if tok.type == TokenType.STRING:
            return self.advance().value
        elif tok.type == TokenType.NUMBER:
            return self.parse_number()
        elif tok.type == TokenType.HEX:
            self.advance()
            return int(tok.value, 16)
        elif tok.type == TokenType.BOOLEAN:
            return self.advance().value == "true"
        elif tok.type == TokenType.IDENTIFIER:
            return self.advance().value
        else:
            raise ParseError(
                f"قيمة غير متوقعة: {tok.type} في السطر {tok.line}"
            )

    def parse_number(self):
        tok = self.peek()
        if tok.type == TokenType.NUMBER:
            self.advance()
            if "." in tok.value:
                return float(tok.value)
            return int(tok.value)
        elif tok.type == TokenType.MINUS:
            self.advance()
            return -self.parse_number()
        else:
            raise ParseError(
                f"متوقع رقم, وجد {tok.type} في السطر {tok.line}"
            )


def parse(tokens):
    return Parser(tokens).parse()
ENDOFFILE

echo "✅ parser.py"
