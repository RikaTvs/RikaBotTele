#!/usr/bin/env bash
# ========================================================
#          RIKA BOT TELE TO AI SERVER (LINUX)
# ========================================================

set -e

# Chuyển về thư mục chứa file script
cd "$(dirname "$0")"

export PYTHONIOENCODING=utf-8
export LANG=C.UTF-8

echo "========================================================"
echo "          RIKA BOT TELE TO AI SERVER (LINUX)"
echo "========================================================"
echo ""

# 1. Kiểm tra Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ [ERROR] Không tìm thấy python3 trên hệ thống!"
    echo "Vui lòng cài đặt bằng lệnh: sudo apt install -y python3 python3-pip python3-venv"
    exit 1
fi

# 2. Quản lý môi trường ảo (virtualenv)
if [ -d "venv" ]; then
    echo "[*] Đang kích hoạt môi trường ảo (venv)..."
    source venv/bin/activate
    PYTHON_BIN="python"
else
    PYTHON_BIN="python3"
fi

# 3. Kiểm tra và cài đặt thư viện phụ thuộc
if [ -f "requirements.txt" ]; then
    echo "[*] Kiểm tra các thư viện phụ thuộc..."
    $PYTHON_BIN -m pip install -r requirements.txt --quiet --disable-pip-version-check || {
        echo "⚠️ [CẢNH BÁO] Không thể tự động cài thư viện qua pip. Vui lòng kiểm tra lại mạng hoặc quyền."
    }
fi

# 4. Đóng các tiến trình bot cũ để tránh lỗi xung đột 409 Conflict
echo "[*] Đang kiểm tra và đóng các tiến trình bot cũ..."
pkill -f "python.*bot\.py" 2>/dev/null || true
sleep 1

# 5. Khởi động Telegram Bot
echo "[*] Đang khởi động Telegram Bot..."
echo ""
exec $PYTHON_BIN bot.py
