#!/usr/bin/env bash
# ========================================================
#           STOP RIKA BOT TELE TO AI (LINUX)
# ========================================================

echo "========================================================"
echo "          ĐANG DỪNG RIKA BOT TELE TO AI"
echo "========================================================"
echo ""

# Đóng tiến trình bot.py
if pkill -f "python.*bot\.py"; then
    echo "[+] Đã dừng toàn bộ tiến trình bot.py thành công!"
else
    echo "[-] Không tìm thấy tiến trình bot.py nào đang chạy."
fi

echo ""
