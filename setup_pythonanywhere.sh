#!/bin/bash
# PythonAnywhere 設置腳本
# 請在 PythonAnywhere 控制台 (Bash) 中執行此腳本

echo "🚀 開始設置 PythonAnywhere..."
echo ""

# 步驟 1: 克隆代碼
echo "Step 1: 克隆 GitHub 倉庫..."
if [ ! -d "szcb-market-api" ]; then
    git clone https://github.com/chanpuirider-design/szcb-market-api.git
fi
cd szcb-market-api

# 步驟 2: 創建虛擬環境
echo "Step 2: 創建虛擬環境..."
python3.11 -m venv venv

# 步驟 3: 激活虛擬環境
echo "Step 3: 激活虛擬環境..."
source venv/bin/activate

# 步驟 4: 安裝依賴
echo "Step 4: 安裝依賴..."
pip install -r requirements.txt

# 步驟 5: 測試
echo "Step 5: 測試應用..."
python -c "from main import app; print('✅ 應用加載成功!')"

echo ""
echo "✅ 設置完成!"
echo ""
echo "下一步:"
echo "1. 進入 PythonAnywhere Web 頁面"
echo "2. 點擊 'Add a new web app'"
echo "3. 選擇 'Manual Config' 和 Python 3.11"
echo "4. 編輯 wsgi.py，將 YOUR_USERNAME 替換為你的用戶名"
echo "5. 點擊 Reload 按鈕"
echo ""
echo "你的 API URL: https://YOUR_USERNAME.pythonanywhere.com"
