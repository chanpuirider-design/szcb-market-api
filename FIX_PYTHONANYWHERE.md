# PythonAnywhere WSGI 配置修復指南

## 錯誤原因
你的 wsgi.py 文件中有一個語法錯誤，第 38 行有單獨的 `python` 字樣。

## 解決方案

### 步驟 1: 修改 wsgi.py
1. 進入 PythonAnywhere **Web** 頁面
2. 點擊 **WSGI configuration file** 連結
3. 替換為以下內容：

```python
import sys
import os

# 配置應用目錄
APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

# 導入 FastAPI 應用
from main import app
application = app
```

### 步驟 2: 保存並重啟
1. 點擊 **Save**
2. 回到 Web 頁面
3. 點擊 **Reload** 按鈕

### 步驟 3: 測試
訪問：https://chanpuirider.pythonanywhere.com/

---

## 備用方案：使用 Git 更新

如果你不想手動編輯，可以：
1. 進入 **Consoles** → **Bash**
2. 執行：
```bash
cd ~/szcb-market-api
git pull
```

然後重新點擊 Web 頁面的 **Reload** 按鈕。
