cat > ~/zalfofont/uninstall.sh << 'SHEOF'
#!/data/data/com.termux/files/usr/bin/bash
#
# zalfofont uninstaller
#

GREEN="\033[92m"
CYAN="\033[96m"
RESET="\033[0m"

echo -e "${CYAN}🗑️  إزالة zalfofont...${RESET}"

# الأمر
rm -f "$PREFIX/bin/zf" 2>/dev/null || true
rm -f "$HOME/.local/bin/zf" 2>/dev/null || true

# المكتبة
pip uninstall zalfofont -y --break-system-packages 2>/dev/null || true

# ملفات مؤقتة
rm -rf "$HOME/.zalfofont" 2>/dev/null || true

echo -e "${GREEN}✅ تم الإزالة${RESET}"
SHEOF

chmod +x ~/zalfofont/uninstall.sh

echo "✅ uninstall.sh"
