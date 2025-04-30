# 救世者之樹主程式自動下載器 / Tree of Savior Auto Downloader

一個用 Python 製作的 GUI 工具，可自動從台灣「救世者之樹」官網擷取主程式安裝檔（exe + bin），支援斷點續傳、多檔並行下載、暫停/繼續、進度顯示與剩餘時間估算。

---

## 📦 功能特色 / Features

- ✅ 自動擷取 Tree of Savior 安裝連結
- ✅ 支援 .exe + 多個 .bin 分段下載
- ✅ 支援斷點續傳 (resume download)
- ✅ 支援暫停 / 繼續下載控制
- ✅ 支援多檔案同時下載（最高 4 檔）
- ✅ 顯示每個檔案的剩餘時間
- ✅ 下載完成自動開啟資料夾
- ✅ GUI 使用 tkinter，無需命令列操作

---

## 📥 安裝與執行方式 / Installation & Execution

### 🔹 方法一：使用 Python 執行

#### 1️⃣ 安裝 Python
請先安裝 Python 3.10 以上版本。

#### 2️⃣ 安裝依賴套件
```bash
pip install -r requirements.txt
```

#### 3️⃣ 執行 GUI 工具
```bash
python tos_downloader_gui.py
```

### 🔹 方法二：使用可執行檔（.exe）

下載 release 中的 `tos_downloader_gui.exe` 並執行，**不需安裝 Python**。

---

## 🛠️ 打包為 exe（開發者用）

```bash
pip install -r requirements.txt
pyinstaller --noconsole --onefile tos_downloader_gui.py
```

打包後 `.exe` 會出現在 `dist/` 資料夾。

---

## 📄 requirements.txt
```txt
requests>=2.31.0
beautifulsoup4>=4.12.2
urllib3>=2.2.1
pyinstaller==5.13.2
tk
```

---

## 🚀 GitLab CI/CD 自動產出 release
請參考 `.gitlab-ci.yml` 設定，自動建立 tag 並將 exe 發佈至 Release 區。

---

## 📝 License
MIT License.

---

# Tree of Savior Auto Downloader (English)

A Python GUI tool to auto-download Taiwan's Tree of Savior full game installer files (.exe + .bin) with pause/resume, multithreading, and download progress tracking.

---

## Features

- ✅ Auto fetch download links from official website
- ✅ Support segmented download (exe + bin)
- ✅ Resume support (HTTP Range)
- ✅ Pause / Resume button
- ✅ Multi-thread download (up to 4)
- ✅ Remaining time estimation per file
- ✅ Auto open download folder on finish
- ✅ Simple GUI (Tkinter-based)

---

## Run Instructions

### 🔹 Method 1: Run via Python
```bash
pip install -r requirements.txt
python tos_downloader_gui.py
```

### 🔹 Method 2: Download .exe release
Download the latest `tos_downloader_gui.exe` from [Releases] and run directly.

---

## Build as .exe (Developer use)
```bash
pyinstaller --noconsole --onefile tos_downloader_gui.py
```

The `.exe` will be generated in `dist/` folder.

---

## License
MIT License