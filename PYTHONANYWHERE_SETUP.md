# SHCB Market Data API - PythonAnywhere 設置指南

## 🚀 快速設置步驟

### Step 1: 上傳代碼到 PythonAnywhere

1. 登錄 https://www.pythonanywhere.com/
2. 進入 **Consoles** → **Bash**
3. 執行以下命令：

```bash
# 克隆 GitHub 倉庫
git clone https://github.com/chanpuirider-design/szcb-market-api.git
cd szcb-market-api

# 創建虛擬環境
python3.11 -m venv venv

# 激活虛擬環境
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

### Step 2: 配置 Web App

1. 進入 **Web** 頁面
2. 點擊 **Add a new web app**
3. 選擇 **Manual Config**
4. 選擇 Python 版本: **3.11**
5. 工作目錄: `/home/YOUR_USERNAME/szcb-market-api`

### Step 3: 配置 WSGI 文件

1. 在 Web 頁面，點擊 **WSGI configuration file** 連結
2. 將以下內容複製並替換：

```python
import sys
import os

# 配置區 - 替換 YOUR_USERNAME
APP_DIR = '/home/YOUR_USERNAME/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from main import app
application = app
```

⚠️ **重要**: 將 `YOUR_USERNAME` 替換為你的 PythonAnywhere 用戶名！

### Step 4: 重啟 Web App

1. 在 Web 頁面點擊 **Reload** 按鈕
2. 等待 10-30 秒
3. 訪問你的網站

### Step 5: 測試 API

```bash
# 在你的瀏覽器中訪問
https://YOUR_USERNAME.pythonanywhere.com/api/stocks
https://YOUR_USERNAME.pythonanywhere.com/api/fx-rates
https://YOUR_USERNAME.pythonanywhere.com/api/yahoo/ticker/HSI
https://YOUR_USERNAME.pythonanywhere.com/docs
```

---

## 📋 檢查清單

- [ ] 已克隆代碼到 PythonAnywhere
- [ ] 已創建虛擬環境
- [ ] 已安裝依賴
- [ ] 已配置 WSGI 文件
- [ ] 已替換 YOUR_USERNAME
- [ ] 已重啟 Web App
- [ ] API 可正常訪問

---

## 🔧 故障排除

### 問題 1: 500 Error
查看錯誤日誌：
1. Web 頁面 → Error logs
2. 常見原因：
   - wsgi.py 中路徑錯誤
   - 依賴未安裝

### 問題 2: 依賴安裝失敗
```bash
# 檢查 Python 版本
python3.11 --version

# 確保在虛擬環境中
source venv/bin/activate
pip install -r requirements.txt
```

### 問題 3: 端口問題
- PythonAnywhere 免費層使用預設端口
- 不需要修改端口配置

---

## 📁 文件說明

| 文件 | 說明 |
|------|------|
| `main.py` | FastAPI 主應用 |
| `requirements.txt` | Python 依賴列表 |
| `wsgi.py` | PythonAnywhere WSGI 配置 |
| `README_PYTHONANYWHERE.md` | 詳細文檔 |

---

## 🔗 有用的鏈接

- PythonAnywhere 控制台: https://www.pythonanywhere.com/user/YOUR_USERNAME/consoles/
- PythonAnywhere Web 頁面: https://www.pythonanywhere.com/user/YOUR_USERNAME/weblications/
- GitHub 倉庫: https://github.com/chanpuirider-design/szcb-market-api
