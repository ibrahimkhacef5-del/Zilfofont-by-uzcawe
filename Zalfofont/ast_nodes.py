cat > zalfofont/ast_nodes.py << 'ENDOFFILE'
"""عقد AST"""


class ASTNode:
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


class Program(ASTNode):
    def __init__(self, font, glyphs):
        self.font = font
        self.glyphs = glyphs


class FontDef(ASTNode):
    def __init__(self, name, properties):
        self.name = name
        self.properties = properties


class GlyphDef(ASTNode):
    def __init__(self, name, properties, contours, anchors):
        self.name = name
        self.properties = properties
        self.contours = contours
        self.anchors = anchors


class Contour(ASTNode):
    def __init__(self, points, closed=False):
        self.points = points
        self.closed = closed


class Point(ASTNode):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Anchor(ASTNode):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
ENDOFFILE

echo "✅ ast_nodes.py"
