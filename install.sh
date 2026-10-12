cat > ~/zalfofont/install.sh << 'SHEOF'
#!/data/data/com.termux/files/usr/bin/bash
#
# zalfofont installer
#

set -e

GREEN="\033[92m"
CYAN="\033[96m"
YELLOW="\033[93m"
RED="\033[91m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${CYAN}${BOLD}"
echo "╔══════════════════════════════════════════╗"
echo "║     zalfofont installer v1.0.0           ║"
echo "║     لغة برمجة للخطوط                     ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${RESET}"

# التحقق
if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${YELLOW}⚠ لست في Termux — التثبيت سيستمر${RESET}"
fi

# 1. المتطلبات
echo -e "${CYAN}[1/4] تحديث المتطلبات...${RESET}"
pkg update -y > /dev/null 2>&1 || true
pkg install -y python git > /dev/null 2>&1

# 2. مكتبات Python
echo -e "${CYAN}[2/4] تثبيت fonttools...${RESET}"
pip install --quiet --upgrade pip
pip install --quiet fonttools

# 3. zalfofont
echo -e "${CYAN}[3/4] تثبيت zalfofont...${RESET}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
pip install -e . --break-system-packages --quiet

# 4. التحقق
echo -e "${CYAN}[4/4] التحقق...${RESET}"
if command -v zf > /dev/null 2>&1; then
    echo -e "${GREEN}✅ zf مثبّت${RESET}"
    zf version
else
    echo -e "${YELLOW}⚠ أعد فتح Terminal${RESET}"
fi

echo ""
echo -e "${GREEN}${BOLD}✅ اكتمل التثبيت!${RESET}"
echo ""
echo -e "${CYAN}جرّب:${RESET}"
echo -e "  ${BOLD}zf --help${RESET}"
echo -e "  ${BOLD}zf build examples/MyFont.zf${RESET}"
echo ""
SHEOF

chmod +x ~/zalfofont/install.sh

echo "✅ install.sh"
