# 🎮 救世者之樹主程式自動下載器 (Tree of Savior Client Auto Downloader)

本專頁是一個圖形化介面（GUI）下載工具，可自動從 Tree of Savior 台服官網採集主程式各分段檔案（.exe 與 .bin），並支援：
- 多檔並行下載 ✅
- 斷點繼傳 ✅
- 暫停與繼續 ✅
- 剩餘時間估算 ✅
- 自動提示完成並打開資料夾 ✅

---

## 🖥️ 執行方式（使用者）

### ✅ 1. 使用打包好的 `.exe` 可執行檔 (適合 Windows 使用者)

> 我們不再直接提供 `.exe` 單檔，以避免被 Defender 或防毒軟體誤認為病毒。

請則下載「壓縮包」：
1. 前往 [Releases](./-/releases)
2. 下載最新版本的 `tos-downloader-vX.X.X.zip`
3. 解壓後執行 `tos_downloader_gui.exe`
4. 請確認\u SHA256 核心檢查碼和原本一致


### 🥍 2. 開發者 / Linux / macOS 用 Python 執行

#### 安裝相依契約：
```bash
pip install -r requirements.txt
```

#### 執行主程式：
```bash
python tos_downloader_gui.py
```

---

## 🛠️ 開發者建議 (打包 .exe)

### 使用 PyInstaller 打包
```bash
pyinstaller --noconsole --onefile tos_downloader_gui.py
```
打包後檔案會在 `dist/tos_downloader_gui.exe`


### 建議重命名並用 ZIP 方式發佈：
```text
release-vX.X.X/
├── tos_downloader_gui.exe
├── README.txt      # 執行說明
├── SHA256.txt      # certutil -hashfile tos_downloader_gui.exe SHA256 產生
```

---

## 🔧 套件需求 (requirements.txt)
```txt
requests>=2.31.0
beautifulsoup4>=4.12.2
urllib3>=2.2.1
pyinstaller==5.13.2
tk
```

---

## 🌐 English Version

# 🎮 Tree of Savior Client Auto Downloader

This Python GUI tool automatically fetches Tree of Savior client chunks (.exe and .bin) from the official download page, with:
- Concurrent download ✅
- Resume support ✅
- Pause & resume ✅
- ETA display ✅
- Folder auto-open after download ✅


## 🖥️ How to Use

### ✅ 1. Windows Users
> We do NOT directly distribute `.exe` to avoid Windows Defender false positives.

Instead:
1. Go to [Releases](./-/releases)
2. Download the latest `tos-downloader-vX.X.X.zip`
3. Extract and run `tos_downloader_gui.exe`
4. Check SHA256 hash for safety


### 🥍 2. Developers or macOS/Linux
```bash
pip install -r requirements.txt
python tos_downloader_gui.py
```


---

## 🛠️ Build EXE (Developer)
```bash
pyinstaller --noconsole --onefile tos_downloader_gui.py
```
Output will be at: `dist/tos_downloader_gui.exe`

To release, zip it with a README + SHA256:
```
tos-downloader-vX.X.X.zip
├── tos_downloader_gui.exe
├── README.txt
├── SHA256.txt
```

---

## 🔧 Requirements
```txt
requests>=2.31.0
beautifulsoup4>=4.12.2
urllib3>=2.2.1
pyinstaller==5.13.2
tk
```

---

## 📄 License
MIT