cat > ~/zalfofont-fix/zalfofont/cli.py << 'PYEOF'
#!/usr/bin/env python3
"""zalfofont CLI - أوامر zf"""
import os
import sys

from .lexer import tokenize, LexerError
from .parser import parse, ParseError
from .compiler import Compiler, CompilerError
from .builder import Builder, BuilderError, build_font


VERSION = "1.0.0"


class C:
    R = "\033[91m"
    G = "\033[92m"
    Y = "\033[93m"
    B = "\033[94m"
    M = "\033[95m"
    CY = "\033[96m"
    W = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"


HELP = f"""
{C.CY}{'═'*58}{C.W}
{C.BOLD}{C.CY}  zalfofont v{VERSION} - لغة برمجة للخطوط{C.W}
{C.CY}{'═'*58}{C.W}

{C.BOLD}الاستخدام:{C.W}
  zf <command> [options]

{C.BOLD}الأوامر:{C.W}
  {C.G}build{C.W} <file.zf> [--output file.ttf]   بناء خط
  {C.G}info{C.W} <file.zf>                          معلومات
  {C.G}check{C.W} <file.zf>                         فحص
  {C.G}tokens{C.W} <file.zf>                        عرض tokens
  {C.G}ast{C.W} <file.zf>                           عرض AST
  {C.G}version{C.W}                                 الإصدار
  {C.G}help{C.W}                                    هذه المساعدة

{C.BOLD}أمثلة:{C.W}
  {C.Y}zf build MyFont.zf{C.W}
  {C.Y}zf build MyFont.zf --output MyFont.ttf{C.W}
  {C.Y}zf info MyFont.zf{C.W}
  {C.Y}zf check MyFont.zf{C.W}
"""


def read_file(path):
    if not os.path.exists(path):
        print(f"{C.R}❌ الملف غير موجود: {path}{C.W}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def compile_source(source):
    try:
        tokens = tokenize(source)
    except LexerError as e:
        print(f"{C.R}❌ خطأ Lexer: {e}{C.W}")
        sys.exit(1)

    try:
        ast = parse(tokens)
    except ParseError as e:
        print(f"{C.R}❌ خطأ Parser: {e}{C.W}")
        sys.exit(1)

    return tokens, ast


def cmd_build(args):
    if not args:
        print(f"{C.R}❌ الاستخدام: zf build <file.zf>{C.W}")
        sys.exit(1)

    src = args[0]
    output = None

    if "--output" in args:
        i = args.index("--output")
        if i + 1 < len(args):
            output = args[i + 1]

    if not output:
        base = os.path.splitext(os.path.basename(src))[0]
        output = f"{base}.ttf"

    print(f"\n{C.CY}{'═'*58}{C.W}")
    print(f"{C.BOLD}{C.CY}  zf build{C.W}")
    print(f"{C.CY}{'═'*58}{C.W}\n")
    print(f"  {C.B}الملف:{C.W}    {src}")
    print(f"  {C.B}المخرج:{C.W}   {output}\n")

    source = read_file(src)

    print(f"{C.CY}[1/4] تحليل...{C.W}")
    tokens, ast = compile_source(source)
    print(f"{C.G}✅ {len(tokens)} tokens{C.W}")

    print(f"{C.CY}[2/4] تجميع...{C.W}")
    try:
        compiler = Compiler()
        font_data = compiler.compile(ast)
    except CompilerError as e:
        print(f"{C.R}❌ خطأ Compiler: {e}{C.W}")
        sys.exit(1)
    print(f"{C.G}✅ {len(font_data['glyphs'])} حروف{C.W}")

    print(f"{C.CY}[3/4] بناء TTF...{C.W}")
    try:
        build_font(font_data, output)
    except BuilderError as e:
        print(f"{C.R}❌ خطأ Builder: {e}{C.W}")
        sys.exit(1)
    except Exception as e:
        print(f"{C.R}❌ خطأ: {e}{C.W}")
        sys.exit(1)

    size = os.path.getsize(output)
    print(f"{C.G}✅ {size//1024}KB{C.W}")

    print(f"{C.CY}[4/4] التحقق...{C.W}")
    print(f"{C.G}✅ الملف موجود{C.W}")

    print(f"\n{C.CY}{'═'*58}{C.W}")
    print(f"{C.BOLD}{C.G}  ✅ انتهى{C.W}")
    print(f"{C.CY}{'═'*58}{C.W}")
    print(f"  {C.G}الملف:{C.W}  {output}")
    print(f"{C.CY}{'═'*58}{C.W}\n")


def cmd_info(args):
    if not args:
        print(f"{C.R}❌ الاستخدام: zf info <file.zf>{C.W}")
        sys.exit(1)

    source = read_file(args[0])
    tokens, ast = compile_source(source)

    print(f"\n{C.CY}{'═'*58}{C.W}")
    print(f"{C.BOLD}{C.CY}  معلومات الخط{C.W}")
    print(f"{C.CY}{'═'*58}{C.W}\n")

    if ast.font:
        print(f"  {C.B}الاسم:{C.W}      {ast.font.name}")
        for key, val in ast.font.properties.items():
            print(f"  {C.B}{key}:{C.W}      {val}")
    else:
        print(f"{C.Y}⚠ الخط غير معرّف{C.W}")

    print(f"\n  {C.B}الحروف:{C.W}     {len(ast.glyphs)}")
    for g in ast.glyphs:
        uv = g.properties.get("unicode", 0)
        print(f"    - {g.name} (U+{uv:04X})")

    print(f"{C.CY}{'═'*58}{C.W}\n")


def cmd_check(args):
    if not args:
        print(f"{C.R}❌ الاستخدام: zf check <file.zf>{C.W}")
        sys.exit(1)

    source = read_file(args[0])
    try:
        tokens, ast = compile_source(source)
        print(f"{C.G}✅ لا أخطاء{C.W}")
        print(f"   tokens: {len(tokens)}")
        print(f"   glyphs: {len(ast.glyphs)}")
    except SystemExit:
        sys.exit(1)


def cmd_tokens(args):
    if not args:
        print(f"{C.R}❌ الاستخدام: zf tokens <file.zf>{C.W}")
        sys.exit(1)

    source = read_file(args[0])
    try:
        tokens = tokenize(source)
    except LexerError as e:
        print(f"{C.R}❌ خطأ: {e}{C.W}")
        sys.exit(1)

    for tok in tokens:
        print(f"  {C.CY}{tok.type:<15}{C.W} "
              f"{C.Y}{tok.value!r:<25}{C.W} "
              f"{C.DIM}{tok.line}:{tok.column}{C.W}")


def cmd_ast(args):
    if not args:
        print(f"{C.R}❌ الاستخدام: zf ast <file.zf>{C.W}")
        sys.exit(1)

    source = read_file(args[0])
    tokens, ast = compile_source(source)
    print(ast)


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("help", "-h", "--help"):
        print(HELP)
        return

    if args[0] in ("version", "-v", "--version"):
        print(f"zalfofont v{VERSION}")
        return

    cmd = args[0]
    rest = args[1:]

    commands = {
        "build": cmd_build,
        "info": cmd_info,
        "check": cmd_check,
        "tokens": cmd_tokens,
        "ast": cmd_ast,
    }

    if cmd in commands:
        commands[cmd](rest)
    else:
        print(f"{C.R}❌ أمر غير معروف: {cmd}{C.W}")
        print(HELP)


if __name__ == "__main__":
    main()
PYEOF

echo "✅ cli.py"
