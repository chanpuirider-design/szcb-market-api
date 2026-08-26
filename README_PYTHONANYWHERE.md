# SHCB Market Data API - PythonAnywhere 部署指南

FastAPI-based market data API for SHCB Risk Analytics Team.

## 🚀 PythonAnywhere 免費部署（不需要信用卡）

### Step 1: 註冊賬戶
1. 訪問 https://www.pythonanywhere.com/registration/
2. 選擇 **"Sign up with GitHub"**（推薦）
3. 完成註冊（不需要信用卡）

### Step 2: 上傳代碼
**方法 A: 使用 Git（推薦）**
```bash
# 進入 PythonAnywhere 控制台 (Bash)
git clone https://github.com/chanpuirider-design/szcb-market-api.git
cd szcb-market-api
```

**方法 B: 下載 ZIP**
1. 訪問 https://github.com/chanpuirider-design/szcb-market-api
2. 點擊 Code → Download ZIP
3. 上傳到 PythonAnywhere 控制台

### Step 3: 配置 Web App
1. 進入 **Web** 頁面
2. 點擊 **Add a new web app**
3. 選擇 **Manual Config**
4. 選擇 Python 版本: **3.11**
5. 工作目錄: `/home/YOUR_USERNAME/szcb-market-api`

### Step 4: 設置虛擬環境
```bash
# 在控制台 Bash 中執行
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5: 配置 WSGI
1. 在 Web 頁面，點擊 **WSGI configuration file** 連結
2. 替換為以下内容：

```python
import sys
import os

# 添加應用目錄
sys.path.insert(0, '/home/YOUR_USERNAME/szcb-market-api')
os.chdir('/home/YOUR_USERNAME/szcb-market-api')

# 導入 FastAPI 應用
from main import app

application = app
```

3. 將 `YOUR_USERNAME` 替換為你的 PythonAnywhere 用戶名

### Step 6: 重啟 Web App
1. 在 Web 頁面點擊 **Reload** 按鈕
2. 等待 10-30 秒
3. 訪問你的網站

### Step 7: 測試 API
```bash
# 你的 API URL
https://YOUR_USERNAME.pythonanywhere.com/api/stocks
https://YOUR_USERNAME.pythonanywhere.com/api/fx-rates
https://YOUR_USERNAME.pythonanywhere.com/api/yahoo/ticker/HSI
https://YOUR_USERNAME.pythonanywhere.com/docs
```

---

## 📋 PythonAnywhere 免費限制

| 限制 | 說明 |
|------|------|
| 網站數量 | 1 個免費網站 |
| CPU 使用 | 限制較低 |
| 記憶體 | 有限 |
| 自定義域名 | 不支援 |
| 數據庫 | 1 個 MySQL 數據庫（可選） |
| Cron Jobs | 支援（每天 1 次） |
| 需要信用卡 | ❌ 不需要 |

---

## 🔧 故障排除

### 問題 1: 500 Error
```bash
# 檢查錯誤日誌
# Web 頁面 → Error logs
```

### 問題 2: 依賴安裝失敗
```bash
# 確保使用正確的 Python 版本
python3.11 --version
pip3.11 install -r requirements.txt
```

### 問題 3: 端口問題
- PythonAnywhere 免費層不允許自定義端口
- 使用預設的 8000 端口

---

## 📁 文件結構

```
szcb-market-api/
├── main.py           # FastAPI 應用
├── requirements.txt  # Python 依賴
├── wsgi.py          # PythonAnywhere WSGI 配置
├── Dockerfile       # Docker 配置（可選）
├── fly.toml         # Fly.io 配置（可選）
└── README.md        # 本文檔
```

---

## 🌟 優點

✅ 完全免費
✅ 不需要信用卡
✅ 簡單的 Web 界面
✅ 內置控制台
✅ 自動 HTTPS
✅ 容易上手

---

## 🔗 相關鏈接

- PythonAnywhere 官網: https://www.pythonanywhere.com/
- 免費層說明: https://www.pythonanywhere.com/pricing/
- FastAPI 文檔: https://fastapi.tiangolo.com/
